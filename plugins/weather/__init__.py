import config
from lib.apis import get_weather

def register(bot):
    bot.register_command('weather', lambda channel, sender, query: get_weather(query) if query else None)
    bot.register_help('weather', '!weather <location> for weather report at specified location.')
