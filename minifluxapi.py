import miniflux
from apikeys import *
from datetime import datetime

client = miniflux.Client(miniflux_url, miniflux_user, miniflux_psw)

def get_new_entries(limit = 1):
    global client

    try:
        entries = client.get_entries(status="unread", limit=limit)["entries"]
    except miniflux.ClientError as err:
        print("miniflux client error: {}".format(err.get_error_reason()), flush=True)
        return None

    response = ""
    for entry in entries:
        publish_date = datetime.strptime(entry["published_at"], "%Y-%m-%dT%H:%M:%SZ")
        publish_date = publish_date.strftime("%Y-%m-%d")
        response += "\x0303[miniflux]\x03 {} {} on {} \x02→\x02 {} \n".format(entry["url"], entry["author"], publish_date, entry["title"])
    
    # mark entries as read
    if entries:
        entry_ids = [entry["id"] for entry in entries]
        client.update_entries(entry_ids, status="read")

    return response

# print(get_new_entries())