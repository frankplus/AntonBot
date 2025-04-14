from lib.apis import Miniflux

def get_miniflux_entries(query):
    try:
        limit = int(query) if query and query.isdigit() else 1
    except Exception:
        limit = 1
    mf = Miniflux()
    response = mf.get_new_entries(limit=limit)
    return response or "No new RSS entries."

def register(bot):
    bot.register_command('miniflux', lambda channel, sender, query: get_miniflux_entries(query))
    bot.register_help('miniflux', '!miniflux [n] to get the latest n RSS entries (default 1).')
