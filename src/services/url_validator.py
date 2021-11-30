from os import getenv
import re
import requests

def validate_url(url):
    pattern = r'(http[s]*|ftp):\/\/[A-Za-z\.\/]*'
    matches = re.match(pattern, url)
    
    if matches and matches[0] == url:
        return True
    return False

def get_url(url):
    if not validate_url(url):
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
