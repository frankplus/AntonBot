from lib.apis import latex_to_text

def register(bot):
    bot.register_command('tex', lambda channel, sender, query: latex_to_text(query) if query else None)
    bot.register_help('tex', '!tex <query> to compile latex into unicode.')
