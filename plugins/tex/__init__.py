import pypandoc

def latex_to_text(formula):
    latex = '${}$'.format(formula)
    try:
        return pypandoc.convert_text(latex, 'plain', format='latex')
    except:
        return None

def register(bot):
    bot.register_command('tex', lambda channel, sender, query: latex_to_text(query) if query else None)
    bot.register_help('tex', '!tex <query> to compile latex into unicode.')
