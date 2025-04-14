from lib.apis import latex_to_png

def register(bot):
    bot.register_command('latex', lambda channel, sender, query: latex_to_png(query) if query else None)
    bot.register_help('latex', '!latex <query> to compile latex into png.')
