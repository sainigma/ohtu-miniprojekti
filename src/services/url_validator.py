import re
from html.parser import HTMLParser
import requests

class TitleMetaGrabber(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = ...):
        super().__init__(convert_charrefs=convert_charrefs)
        self.title = 'No title found'
        self.meta = []
        self.grabbing = None
        self.failure = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str or None]]):
        if tag == 'title':
            self.grabbing = tag
        elif 'meta' in tag:
            self.meta.append(attrs)

    def handle_data(self, data: str):
        if self.grabbing is None:
            return
        if self.grabbing == 'title':
            self.title = data
    
    def error(self, message: str) -> None:
        self.failure = True

    def success(self):
        return not self.failure

    # nestaamisesta ei tarvitse välittää, title ja meta on void elementtejä
    def handle_endtag(self, tag: str):
        if self.grabbing is None:
            return
        if tag == self.grabbing:
            self.grabbing = None

    def parse_data(self, data):
        self.feed(data)
    
    def get_title(self):
        return self.title

    def get_meta(self):
        return self.meta

def validate_url(url):
    pattern = r'(http[s]*|ftp):\/\/[A-Za-z0-9\-\.\/]*'
    matches = re.match(pattern, url)
    
    if matches and matches[0] == url:
        return True
    return False

def parse_results(response : requests.Response):
    parser = TitleMetaGrabber()
    parser.parse_data(response.content.decode(response.encoding))
    if parser.success():
        return {
            'title':parser.get_title(),
            'meta':parser.get_meta()
        }
    return None

def get_url(url):
    if not validate_url(url):
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return parse_results(response)
        return None
    except requests.ConnectionError:
        return None
