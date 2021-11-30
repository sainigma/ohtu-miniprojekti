import re
import requests

def _validate_url(url):
    pattern = r'(http[s]*|ftp):\/\/[A-Za-z\.\/]*'
    matches = re.match(pattern, url)
    
    if matches and matches[0] == url:
        return True
    return False

def _get_url(url):
    if not _validate_url(url):
        return None
    try:
        result = requests.get(url)
        if result.status_code == 200:
            return {
                'headers':result.headers,
                'content':result.content,
                'status':200
            }
        return None
    except requests.ConnectionError as exception:
        return False

def _fake_validate_url(url):
    return True

get_url = _validate_url
