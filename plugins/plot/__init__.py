import urllib

def plot_function(query):
    q = {'q': query}
    q = urllib.parse.urlencode(q)
    return f'https://frankplus.github.io/plasm?{q}'

def register(bot):
    bot.register_command('plot', lambda channel, sender, query: plot_function(query) if query else None)
    bot.register_help('plot', '!plot <query> to plot any mathematical function.')
