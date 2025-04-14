import config

def set_bot_autospeak(autospeak):
    config.AUTO_SPEAK = autospeak
    if autospeak:
        return "I will join your conversations"
    else:
        return "I'll be quiet then"

def register(bot):
    bot.register_command('talk', lambda channel, sender, query: set_bot_autospeak(True))
    bot.register_help('talk', '!talk if you want me to participate in your conversations')
