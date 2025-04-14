import requests
from bs4 import BeautifulSoup

def get_latest_news(query):
    url = f"https://news.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('a', class_='DY5T1d')
    return [headline.text for headline in headlines[:5]]

def register(bot):
    bot.register_command('news', lambda channel, sender, query: get_latest_news(query))
    bot.register_help('news', '!news <query> for latest news related to specified query.')