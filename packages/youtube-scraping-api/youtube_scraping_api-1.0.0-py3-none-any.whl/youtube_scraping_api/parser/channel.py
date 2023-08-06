import requests
from ..constants import HEADERS
from ..utils import searchDict, revealRedirectUrl, getInitialData
from ..urls import *

class Author:
    def __init__(self, name, url, channel_id):
        self.name = name
        self.url = url
        self.channel_id = channel_id

    def __repr__(self):
        return f'<Channel name="{self.name}">'

    @property
    def raw(self):
        return {
            "name": self.name,
            "url": self.url,
            "channel_id": self.channel_id
        }

class Channel:
    def __init__(self, channel_id=None, username=None, builtin_called=False, **kwargs):
        self._session = requests.Session()
        self._session.headers = HEADERS

        self.id = channel_id
        self.username = username

        self.data = None
        self.about_data = None
        self._raw_metadata = None
        self._raw_header = None
        self._is_builtin_callled = builtin_called

        self.static_properties = kwargs

        self.properties = {
            'id': (lambda x: x["externalId"], 'raw_metadata'),
            'name': (lambda x: x["title"], 'raw_metadata'),
            'description': (lambda x: x["description"], 'raw_metadata'),
            'keywords': (lambda x: x["keywords"].split() if "keywords" in x else None, 'raw_metadata'),
            'url': (lambda x: x["channelUrl"], 'raw_metadata'),
            'vanity_url': (lambda x: x["vanityChannelUrl"], 'raw_metadata'),
            'facebook_profile_id': (lambda x: x["facebookProfileId"] if "facebookProfileId" in x else None, 'raw_metadata'),
            'avatar': (lambda x: x["avatar"]["thumbnails"][0], 'raw_metadata'),
            'subscriber_count': (lambda x: self._subscriber_count(x), 'raw_header'),
            'banner': (lambda x: self._banner(x), 'raw_header'),
            'header_links': (lambda x: self._header_links(x), 'raw_header'),
            'is_verified': (lambda x: self._is_verified(x), 'raw_header')
        }

    def _parseData(self, channel_id, username):
        if not (channel_id or username): return {}
        if channel_id: url = (
            CHANNEL_ID_URL+channel_id, 
            CHANNEL_ID_URL+channel_id+"/about"
        )
        elif username: url = (
            CHANNEL_USERNAME_URL+username, 
            CHANNEL_USERNAME_URL+username+"/about"
        )
        response = [self._session.get(i).text for i in url]
        if "404 Not Found" in response[0]:
            self._debug("ERROR", "Channel not exist")
            return
        self.data, self.about_data = (getInitialData(i) for i in response)
        self._raw_metadata = self.data["metadata"]["channelMetadataRenderer"]
        self._raw_header = self.data["header"]

    def __getattr__(self, attr):
        try:
            if self._is_builtin_callled and attr in self.static_properties:
                return self.static_properties[attr]
            elif attr in self.properties: 
                func, *var = self.properties[attr]
                if not eval(f'self._{var[0]}'): self._parseData(self.id, self.username)
                var = [eval(f'self._{v}', {'self': self}) for v in var]
                return func(*var)
            return self.__dict__[attr]
        except (KeyError, ValueError, AttributeError):
            raise AttributeError(f'Attribute {attr} not exist')

    def _subscriber_count(self, x):
        try: subscriber_count = next(searchDict(x, "subscriberCountText"))["simpleText"].split()[0]
        except: subscriber_count = "No"
        return int(subscriber_count) if subscriber_count.isdigit() else None if subscriber_count == "No" else subscriber_count

    def _banner(self, x):
        try: return next(searchDict(x, "banner"))["thumbnails"]
        except: return None

    def _header_links(self, x):
        try:
            _raw_header_links = next(searchDict(x, "channelHeaderLinksRenderer")).values()
            header_links = [{
                "title": i["title"]["simpleText"],
                "icon": i["icon"]["thumbnails"][0]["url"],
                "url": revealRedirectUrl(i["navigationEndpoint"]["urlEndpoint"]["url"])
            } for i in sum(_raw_header_links, [])]
            return header_links
        except:
            return None

    def _is_verified(self, x):
        try:
            if next(searchDict(x, "badges"))[0]["metadataBadgeRenderer"]["tooltip"] == "Verified":
                return True
            return False
        except: return False

    def __repr__(self):
        return f'<Channel id="{self.id}" name="{self.name}">'
