def register(bot):
    bot.register_command('tell', lambda channel, sender, query: bot.get_bot_instance(channel).add_tell(query) if query else None)
    bot.register_help('tell', '!tell <recipient> <message> to tell a message when the recipient joins the channel')
