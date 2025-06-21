import requests
from bs4 import BeautifulSoup

# Function definition for OpenAI function calling
NEWS_FUNCTION_DEFINITION = {
    "type": "function",
    "function": {
        "name": "get_latest_news",
        "description": "Get the latest news articles. Can search for specific topics or get general top headlines from Italy.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Optional search query for specific news topics. If not provided, returns top headlines from Italy."
                }
            },
            "required": []
        }
    }
}

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