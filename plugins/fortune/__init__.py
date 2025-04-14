from lib.utils import json_request_get

def fortune():
    return json_request_get("http://yerkee.com/api/fortune")['fortune']

def register(bot):
    bot.register_command('fortune', lambda channel, sender, query: fortune())
    bot.register_help('fortune', '!fortune try this command yourself ;)')
