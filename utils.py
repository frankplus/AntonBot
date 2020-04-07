import requests
from requests.exceptions import Timeout

def json_request(url):
    try:
        r = requests.get(url, timeout=5)
    except Timeout:
        print('The request timed out. url: {}'.format(url))
        return None

    if not r:
        print("Error requesting {} status code = {}".format(url, r.status_code))
        return None

    return r.json()