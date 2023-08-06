import json
import string
import requests
from bs4 import BeautifulSoup as bs
from .constants import HEADERS, THUMBNAIL_TEMPLATE

def searchDict(partial, key):
        if isinstance(partial, dict):
            for k, v in partial.items():
                if k == key:
                    yield v
                else:
                    for o in searchDict(v, key):
                        yield o
        elif isinstance(partial, list):
            for i in partial:
                for o in searchDict(i, key):
                    yield o

def findSnippet(text, snippet, end_delimeter, skip=(0, 0)):
        start = text.find(snippet)
        if start == -1: return start
        end = text.find(end_delimeter, start)
        return text[start+len(snippet)+skip[0]:end-skip[1]]

def parseContinuationToken(data):
        try: nextCT = next(searchDict(data, "token"))
        except: nextCT = None
        finally: return nextCT

def convertValidFilename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c for c in s if c in valid_chars)

getInitialData = lambda html: json.loads(findSnippet(html, "var ytInitialData = ", "</script>", (0, 1)))
getInitialPlayerResponse = lambda html: json.loads(findSnippet(html, "var ytInitialPlayerResponse = ", ";</script>", (0, 1))+"}", strict=False)
revealRedirectUrl = lambda url: bs(requests.get(url, headers=HEADERS).content, "lxml").find("div", {"id": "redirect-action-container"}).find("a")["href"]
getThumbnail = lambda videoId: dict(map(lambda i: (i[0], i[1].format(videoId)), THUMBNAIL_TEMPLATE.items()))