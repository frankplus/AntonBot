from lib.apis import tweet

def register(bot):
    bot.register_command('tweet', lambda channel, sender, query: tweet(query))
    bot.register_help('tweet', '!tweet <message> to tweet a message')
