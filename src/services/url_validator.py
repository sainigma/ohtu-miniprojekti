import re
from html.parser import HTMLParser
import requests

class UrlCache():
    def __init__(self):
        self.cache = {}

    def append(self, url, response):
        self.cache[url] = response

    def has(self, url):
        if url in self.cache:
            return True
        return False

    def get(self, url):
        return self.cache[url]

class TitleMetaGrabber(HTMLParser):

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = 'No title found'
        self.meta = []
        self.grabbing = None
        self.failure = False

    # tag: str, attrs: list[tuple[str, str or None]]
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.grabbing = tag
        elif 'meta' in tag:
            self.meta.append(attrs)

    def handle_data(self, data: str):
        if self.grabbing is None:
            return
        if self.grabbing == 'title':
            self.title = data
    
    def error(self, message: str):
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
    # https://www.gamasutra.com/view/news/249475/More_dirty_coding_tricks_from_game_developers.php#:~:text=Thanks%20for%20playing!
    pattern = r'(http[s]*|ftp):\/\/[A-Za-z0-9_%&:?!#=()+~\-\.\/]*'
    matches = re.match(pattern, url)
    
    if matches and matches[0] == url:
        return True
    return False

def parse_results(response : requests.Response):
    parser = TitleMetaGrabber()
    if response.encoding is None:
        return {
            'title':'URL is a file',
            'meta':[]
        }
    try:
        parser.parse_data(response.content.decode(response.encoding))
    except UnicodeDecodeError:
        return {
            'title':'Extremely rare header/content encoding mismatch detected! :D',
            'meta':[]
        }
    if parser.success():
        return {
            'title':parser.get_title(),
            'meta':parser.get_meta()
        }
    return None

def get_url(url):
    if url_cache.has(url):
        return url_cache.get(url)
    if not validate_url(url):
        url_cache.append(url, None)
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = parse_results(response)
            url_cache.append(url, result)
            return result
        url_cache.append(url, None)
        return None
    except requests.ConnectionError:
        url_cache.append(url, None)
        return None

url_cache = UrlCache()