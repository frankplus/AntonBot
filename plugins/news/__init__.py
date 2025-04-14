import requests
from bs4 import BeautifulSoup

def get_latest_news(query=None):
    if query:
        url = f'http://newsapi.org/v2/everything?q={query}&sortBy=relevancy&apiKey=' + __import__('config').NEWSAPI_KEY
    else:
        url = 'http://newsapi.org/v2/top-headlines?country=it&sortBy=publishedAt&apiKey=' + __import__('config').NEWSAPI_KEY
    data = __import__('lib.utils').utils.json_request_get(url)
    if not data:
        return None
    if data["status"] == "ok" and data["totalResults"] > 0:
        article = data["articles"][0]
        description = article["description"].replace('\n', ' ')
        info = '{} - {}'.format(article["url"], description)
        return info
    else:
        return "I haven't found anything"

def register(bot):
    bot.register_command('news', lambda channel, sender, query: get_latest_news(query))
    bot.register_help('news', '!news <query> for latest news related to specified query.')