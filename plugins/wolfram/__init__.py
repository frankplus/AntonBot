from lib.apis import wolfram_req

def register(bot):
    bot.register_command('wolfram', lambda channel, sender, query: wolfram_req(query) if query else None)
    bot.register_help('wolfram', '!wolfram <query> to calculate or ask any question.')
