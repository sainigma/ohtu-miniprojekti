import requests

def validate_url(url):
    try:
        requests.get(url)
        return True
    except requests.ConnectionError as exception:
        return False
        