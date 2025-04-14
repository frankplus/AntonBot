import requests

def latex_to_png(formula):
    formula = "\\bg_ffffff {}".format(formula)
    r = requests.get('http://latex.codecogs.com/png.latex?\dpi{{300}} {formula}'.format(formula=formula))
    return r.url

def register(bot):
    bot.register_command('latex', lambda channel, sender, query: latex_to_png(query) if query else None)
    bot.register_help('latex', '!latex <query> to compile latex into png.')
