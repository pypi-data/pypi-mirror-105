import requests
import itertools
from .parser.search_result import SearchResult, cleanupData as cleanupVideoData
from .parser.playlist import Playlist, cleanupData as cleanupPlaylistData
from .parser.video import Video
from .parser.channel import Channel
from .urls import *
from .constants import PAYLOAD, HEADERS
from .utils import *
from .decorators import *
from .filter import *

class YoutubeAPI:
    _data = PAYLOAD

    @logException
    def __init__(self, debug_level="ERROR"):
        self._session = requests.Session()
        self._session.headers = HEADERS
        self._debug_level = debug_level
        try: raw = self._session.get("https://www.youtube.com").text
        except: raise RuntimeError("Please check your internet connection")
        
        self.DEBUG_LEVEL = dict([i[::-1] for i in enumerate(["INFO", "SUCCESS", "WARNING", "ERROR"])])
        self.API_TOKEN = findSnippet(raw, "innertubeApiKey", ",", (3, 1))

    def search(self, query=None, continuation_token=None, raw=False, filter=None):
        if not (query or continuation_token): return None

        if query:
            base_url = SEARCH_BASE_URL+"+".join(query.split())
            if filter and isinstance(filter, SearchFilter): final_url = getFilteredURL(self._session, base_url, filter)
            else: final_url = base_url
            html = self._session.get(final_url).text
            response = getInitialData(html)
        
        elif continuation_token:
            self._data["continuation"] = continuation_token
            response = self._session.post(SEARCH_CONTINUATION_URL+self.API_TOKEN, json=self._data).json()

        nextCT = parseContinuationToken(response)
        
        if query:
            data = [next(searchDict(i, "contents")) for i in searchDict(response,"itemSectionRenderer")]
            result = SearchResult(itertools.chain(*[cleanupVideoData(i) for i in data]), nextCT)
            result.url = final_url
        
        if continuation_token:
            try: data = next(searchDict(response, "contents"))
            except: data = next(searchDict(response, "continuationItems"))
            result = cleanupVideoData(data, nextCT, to_object=True)
        
        if not raw: return result
        else: return result.raw

    @logException
    def playlist(self, playlistId=None, continuation_token=None, parseAll=True):
        if not (playlistId or continuation_token): return None

        if playlistId:
            html = self._session.get(PLAYLIST_BASE_URL+playlistId).text
            response = getInitialData(html)

        elif continuation_token:
            if not continuation_token: return {}, None
            self._data["continuation"] = continuation_token
            response = self._session.post(PLAYLIST_CONTINUTION_URL+self.API_TOKEN, json=self._data).json()

        nextCT = parseContinuationToken(response)

        if playlistId: 
            result = Playlist(response)
        
        elif continuation_token: 
            data = next(searchDict(response, "continuationItems"))
            result = cleanupPlaylistData(data)

        if parseAll:
            while nextCT:
                response, nextCT = self.playlist(continuation_token = nextCT)
                result += response

        if playlistId: return result
        elif continuation_token: return result, nextCT

    @logException
    def channel(self, channel_id=None, username=None):
        result = Channel(channel_id=channel_id, username=username)
        return result

    @logException
    def video(self, video_id):
        return Video(video_id)

    @logException
    def _debug(self, level ,text):
        if self.DEBUG_LEVEL[level] >= self.DEBUG_LEVEL[self._debug_level]:
            if level == "ERROR":
                print("[-] ERROR:", text)
            elif level == "WARNING":
                print("[!] WARNING:", text)
            elif level == "INFO":
                print("[*] INFO:", text)
            elif level == "SUCCESS":
                print("[+] SUCCESS:", text)
