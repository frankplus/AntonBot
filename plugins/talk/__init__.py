def register(bot):
    bot.register_command('talk', lambda channel, sender, query: set_bot_autospeak(True))
    bot.register_help('talk', '!talk if you want me to participate in your conversations')
