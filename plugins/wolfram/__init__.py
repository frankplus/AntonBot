from config import WOLFRAM_KEY
from lib.utils import http_request_get

def wolfram_req(query):
    url = f'https://api.wolframalpha.com/v1/result?i={query}&appid={WOLFRAM_KEY}'
    resp = http_request_get(url)
    if resp:
        return resp.text.replace('\n', '. ')

def register(bot):
    bot.register_command('wolfram', lambda channel, sender, query: wolfram_req(query) if query else None)
    bot.register_help('wolfram', '!wolfram <query> to calculate or ask any question.')
