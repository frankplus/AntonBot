import miniflux
import datetime
import logging
import config

def get_miniflux_entries(query):
    try:
        limit = int(query) if query and query.isdigit() else 1
    except Exception:
        limit = 1
    mf = Miniflux()
    response = mf.get_new_entries(limit=limit)
    return response or "No new RSS entries."

class Miniflux:
    def __init__(self):
        self.client = miniflux.Client(config.MINIFLUX_URL, config.MINIFLUX_USER, config.MINIFLUX_PSW)

    def get_new_entries(self, limit = 1):
        try:
            entries = self.client.get_entries(status="unread", limit=limit)["entries"]
        except miniflux.ClientError as err:
            logging.error("miniflux client error: {}".format(err.get_error_reason()))
            return None
        except:
            logging.exception("Unexpected error getting RSS entries")
            return None
        response = ""
        for entry in entries:
            try:
                publish_date = datetime.datetime.strptime(entry["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                publish_date = datetime.datetime.strptime(entry["published_at"], "%Y-%m-%dT%H:%M:%SZ")
            publish_date = publish_date.strftime("%Y-%m-%d")
            response += "\x0303[miniflux]\x03 {} {} on {} \x02→\x02 {} \n".format(entry["url"], entry["author"], publish_date, entry["title"])
        # mark entries as read
        if entries:
            entry_ids = [entry["id"] for entry in entries]
            self.client.update_entries(entry_ids, status="read")
        return response

def register(bot):
    bot.register_command('miniflux', lambda channel, sender, query: get_miniflux_entries(query))
    bot.register_help('miniflux', '!miniflux [n] to get the latest n RSS entries (default 1).')
