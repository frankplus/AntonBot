def register(bot):
    bot.register_command('shush', lambda channel, sender, query: set_bot_autospeak(False))
    bot.register_help('shush', '!shush to make me stop being annoying')
