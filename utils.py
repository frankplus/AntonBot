import requests
from requests.exceptions import Timeout
import traceback

channel = "#bugbyte-ita"
botname = "CovidBot"
irc_server_address = "irc.freenode.net"

def json_request(url, headers=None):
    try:
        r = requests.get(url, timeout=5, headers=headers)
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

    return r.json()