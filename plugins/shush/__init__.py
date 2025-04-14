import config

def set_bot_autospeak(autospeak):
    config.AUTO_SPEAK = autospeak
    if autospeak:
        return "I will join your conversations"
    else:
        return "I'll be quiet then"

def register(bot):
    bot.register_command('shush', lambda channel, sender, query: set_bot_autospeak(False))
    bot.register_help('shush', '!shush to make me stop being annoying')
