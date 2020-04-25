import requests
from requests.exceptions import Timeout
import traceback
from config import HTTP_REQUEST_TIMEOUT

def json_request(url):
    return http_request(url, json=True)

def http_request(url, json=False, headers=None):

    try:
        r = requests.get(url, timeout=HTTP_REQUEST_TIMEOUT, headers=headers)
    except Timeout:
        print('The request timed out. url: {}'.format(url))
        return None
    except:
        print('Error requesting url: {}'.format(url))
        print(traceback.format_exc())
        return None

    if not r:
        print("Error requesting {} status code = {}".format(url, r.status_code))
        return None

    return r.json() if json else r