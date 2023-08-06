import requests
import os
import string
from urllib.parse import parse_qs
from tqdm import tqdm
import copy
from bs4 import BeautifulSoup as bs
from ..cipher import Cipher
from ..urls import *
from ..utils import *
from ..decorators import *
from ..constants import HEADERS
from .channel import Author

class Video():

    @logException
    def __init__(self, videoId, builtin_called=False, **kwargs):
        self._session = requests.Session()
        self._session.headers = HEADERS

        self._raw = None
        self._player_data = None
        self._init_data = None
        self._primary_info = None
        self._secondary_info = None
        self._player_info = None
        self._is_builtin_callled = builtin_called

        self.id = videoId
        self.thumbnails = getThumbnail(self.id)

        self.static_properties = kwargs
        self.properties = {
            'title': (lambda x: "".join(i["text"] for i in x["title"]["runs"]), 'primary_info'),
            "type": (lambda x: "livestream" if "isLive" in x["viewCount"]["videoViewCountRenderer"] and x["viewCount"]["videoViewCountRenderer"]["isLive"] else "video", 'primary_info'),
            "supertitle": (lambda x: self.getSupertitle(x), 'primary_info'),
            "description": (lambda x: "".join(i["text"] for i in x["description"]["runs"]) if "description" in x else None, 'secondary_info'),
            "tags": (lambda x: x["keywords"] if "keywords" in x else None, 'player_info'),
            "publish_time": (lambda x: x["dateText"]["simpleText"], 'primary_info'),
            "author": (lambda x, y: Author(
                x["author"],
                y["owner"]["videoOwnerRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
                x["channelId"]
            ), 'player_info', 'secondary_info'),
            "length": (lambda x: int(x["lengthSeconds"]), 'player_info')
        }

    def __repr__(self):
        return f'<Video id="{self.id}" title="{self.title}" author="{self.author.name}">'

    def __getattr__(self, attr):
        try:
            if self._is_builtin_callled and attr in self.static_properties:
                return self.static_properties[attr]
            elif attr in self.properties: 
                func, *var = self.properties[attr]
                if not eval(f'self._{var[0]}'): self._parseData()
                var = [eval(f'self._{v}', {'self': self}) for v in var]
                return func(*var)
            return self.__dict__[attr]
        except (KeyError, ValueError, AttributeError):
            raise AttributeError(f'Attribute {attr} not exist')

    def _parseData(self):
        self._raw = self._session.get(VIDEO_PLAYER_URL+self.id).text
        self._player_data = getInitialPlayerResponse(self._raw)
        self._init_data = getInitialData(self._raw)
        self._primary_info = next(searchDict(self._init_data, "videoPrimaryInfoRenderer"))
        self._secondary_info = next(searchDict(self._init_data, "videoSecondaryInfoRenderer"))
        self._player_info = self._player_data["videoDetails"]

    @logException
    def _getSignatureUrl(self, url):
        base_url = findSnippet(self._raw, "jsUrl", ",", (3, 1))
        js_url = BASE_URL+base_url
        js_content = self._session.get(js_url).text
        cipher = Cipher(js_content)
        s, sp, url = [i[0] for i in parse_qs(url).values()]
        return url + "&sig=" + cipher.get_signature(s)
    
    @logException
    def _getCommentCount(self):
        continuation = next(searchDict(self._init_data, 'nextContinuationData'))['continuation'].replace('%3D', '=')
        xsrf_token = findSnippet(self._raw, 'XSRF_TOKEN', ",", (3, 1)).replace(r'\u003d', '\u003d')
        params = {
            'action_get_comments': 1,
            'pbj': 1,
            'ctoken': continuation,
            'continuation': continuation,
            'type': 'next'
        }
        data = self._session.post(COMMENT_AJAX_URL, data={'session_token': xsrf_token}, params=params).json()
        comment_count = int(next(searchDict(data, 'countText'))['runs'][0]['text'].replace(',', ''))
        return comment_count

    @logException
    def getSupertitle(self, primary_info):
        if not "superTitleLink" in primary_info: return None
        supertitle = [{
            'text': i['text'].strip(),
            'url': next(searchDict(i, 'url'))
        } for i in primary_info["superTitleLink"]["runs"] if i['text'].strip()] 
        return supertitle 

    @property
    @logException
    def raw(self):
        if not self._primary_info: self._parseData()
        primary_info = self._primary_info
        player_info = self._player_info
        cleaned_data = {
            "video_id": self.id,
            "type": self.type,
            "title": self.title,
            "supertitle": self.supertitle,
            "description": self.description,
            "tags": self.tags,
            "publish_time": self.publish_time,
            "author": self.author.raw,
            "length": self.length,
            "thumbnails": self.thumbnails,
            "statistics": {
                "view_count": int(player_info["viewCount"]),
                **dict(zip(["like_count", "unlike_count"], map(lambda i: int(i.replace(",", "")), primary_info["sentimentBar"]["sentimentBarRenderer"]["tooltip"].split(" / ")))),
                "comment_count": self._getCommentCount()
            }
        }
        return cleaned_data

    @property
    @logException
    def download_data(self):
        if not self._player_data: self._parseData()
        return dict([(i["itag"], {
            "url": i["url"] if "url" in i else None,
            'signature_cipher': i["signatureCipher"] if "signatureCipher" in i else None,
            "mime_type": i["mimeType"],
            "bitrate": i["bitrate"],
            "width": i["width"] if "width" in i else None,
            "height": i["height"] if "height" in i else None,
            "size": i["contentLength"] if "contentLength" in i else None,
            "fps": i["fps"] if "fps" in i else None,
            "quality": i["quality"],
            "quality_label": i["qualityLabel"] if "qualityLabel" in i else None,
            "duration": i["approxDurationMs"] if "approxDurationMs" in i else None
        }) for i in self._player_data["streamingData"]["formats"]+self._player_data["streamingData"]["adaptiveFormats"]]) if self.type!="livestream" else None

    @logException
    def _getFileSize(self, url):
        return int(self._session.get(url, stream=True).headers.get('content-length', 0))

    @logException
    def _stream(self, url, chunk_size=4096, range_size=9437184):
        file_size: int = self._getFileSize(url)
        downloaded = 0
        while downloaded < file_size:
            stop_pos = min(downloaded + range_size, file_size) - 1
            range_header = f"bytes={downloaded}-{stop_pos}"
            response = requests.get(url, headers={"Range": range_header}, stream=True)
            for chunk in response.iter_content(chunk_size):
                if not chunk: break
                downloaded += len(chunk)
                yield chunk
        return

    @logException
    def download(self, itag=None, path=".", log_progress=True, chunk_size=4096, callback_func=None, name=None):
        if itag:
            if itag in self.download_data.keys(): target = self.download_data[itag]
            else: raise RuntimeError('Itag not exist!')
        else: target = list(self.download_data.values())[0]

        if target['url'] != None: target_url = target['url']
        elif target["signature_cipher"]: 
            target_url = self._getSignatureUrl(target["signature_cipher"])
        vid_name = name if name else convertValidFilename(self.title)
        extension = target["mime_type"].split(";")[0].split("/")[-1]
        print(self.title)
        if log_progress: progress_bar = tqdm(total=self._getFileSize(target_url), unit='iB', unit_scale=True)
        with open(os.path.join(path, f"{vid_name}.{extension}"), "wb") as f:
            for chunk in self._stream(target_url, chunk_size=chunk_size):
                if log_progress: progress_bar.update(len(chunk))
                f.write(chunk)

    @property
    def captions(self):
        if not self._player_data: self._parseData()
        if not "captions" in self._player_data: return None
        raw = self._player_data["captions"]["playerCaptionsTracklistRenderer"]
        default_raw = raw["audioTracks"][0]
        default = default_raw["defaultCaptionTrackIndex"] if "defaultCaptionTrackIndex" in default_raw else 0
        caption_list = raw["captionTracks"]
        result = CaptionQuery((Caption(i["languageCode"], i["name"]["simpleText"], i["baseUrl"], i["isTranslatable"], raw["translationLanguages"]) for i in caption_list), default)
        return result

class TranslationLang:
    def __init__(self, raw):
        self.name = raw["languageName"]["simpleText"]
        self.language_code = raw["languageCode"]

    def __repr__(self):
        return f'<TranslationLang name="{self.name}" code="{self.language_code}">'

class CaptionQuery(list):
    def __init__(self, data, default=0):
        super(CaptionQuery, self).__init__(data)
        self.default=default

    def get_caption(self, language_code=None):
        if not language_code:
            return self[self.default]
        else:
            for i in self:
                if i.language_code == language_code:
                    return i

class TranslangQuery(list):
    def __init__(self, data):
        super(TranslangQuery, self).__init__(data)

    def get_language(self, language_code):
        for i in self:
            if i.language_code == language_code:
                return i

    def get_name(self):
        return [i.name for i in self]

    def get_language_code(self):
        return [i.language_code for i in self]

class Caption():
    def __init__(self, language_code, name ,url, translatable=False, translate_langs=None):
        self.language_code = language_code
        self.name = name
        self._url = url
        self.is_translatable = translatable
        self._trans_lang = translate_langs
    
    def __repr__(self):
        return f'<Caption lang="{self.name}" code="{self.language_code}" is_translatable={self.is_translatable}>'

    @property
    def available_translations(self):
        if self.is_translatable:
            return TranslangQuery(TranslationLang(i) for i in self._trans_lang)

    @property
    def xml(self):
        return requests.get(self._url).text

    def get_text(self, delimiter='\n'):
        raw = bs(self.xml, 'lxml')
        text = raw.findAll('text')
        string = [bs(i.text, 'lxml').text for i in text]
        return delimiter.join(string)

    @property
    def dict(self):
        raw = bs(self.xml, 'lxml')
        text = raw.findAll('text')
        return [{
            'start_from': float(i['start']),
            'duration': float(i['dur']),
            'text': bs(i.text, 'lxml').text
        } for i in text]

    def translate_to(self, language_code):
        if self.is_translatable:
            if not language_code in self.available_translations.get_language_code():
                return None
            return TranslatedCaption(self.available_translations.get_language(language_code), self._url, self.language_code)

class TranslatedCaption(Caption):
    def __init__(self, language ,url, original_lang_code):
        super(TranslatedCaption, self).__init__(language.language_code, language.name , url)
        del Caption.translate_to

        self.language_code = language.language_code
        self.name = language.name
        self._url = url+'&tlang='+self.language_code
        self.original_language_code = original_lang_code
    
    def __repr__(self):
        return f'<TranslatedCaption lang="{self.name}" code="{self.language_code}" translated_from="{self.original_language_code}">'