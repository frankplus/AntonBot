from lib.apis import fortune

def register(bot):
    bot.register_command('fortune', lambda channel, sender, query: fortune())
    bot.register_help('fortune', '!fortune try this command yourself ;)')
