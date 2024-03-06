import requests
from requests.exceptions import Timeout
import traceback
from config import HTTP_REQUEST_TIMEOUT
import logging

def json_request_get(url, timeout=None):
    return http_request_get(url, json=True, timeout=timeout)

def http_request_get(url, json=False, headers=None, timeout=None):

    try:
        r = requests.get(url, timeout=timeout if timeout else HTTP_REQUEST_TIMEOUT, headers=headers)
    except Timeout:
        logging.error('The request timed out. url: {}'.format(url))
        return None
    except:
        logging.exception('Error requesting url: {}'.format(url))
        return None

    if not r:
        logging.error("Error requesting {} status code = {}".format(url, r.status_code))
        return None

    return r.json() if json else r

def http_request_post(url, json_data, json=False, headers=None, timeout=None):

    try:
        r = requests.post(url, json=json_data, timeout=timeout if timeout else HTTP_REQUEST_TIMEOUT, headers=headers)
    except Timeout:
        logging.error('The request timed out. url: {}'.format(url))
        return None
    except:
        logging.exception('Error requesting url: {}'.format(url))
        return None

    if not r:
        logging.error("Error requesting {} status code = {}".format(url, r.status_code))
        return None

    return r.json() if json else r
