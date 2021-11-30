import requests

def _validate_url(url):
    try:
        requests.get(url)
        return True
    except requests.ConnectionError as exception:
        return False

def _fake_validate_url(url):
    return True

validate_url = _validate_url