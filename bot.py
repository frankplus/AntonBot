from apis import *
import random
import corona

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup?"
]

def elaborate_query(sender, message):
    message = message.strip()
    if message.lower() in ["hi", "hello", "yo", "hey"]:
        return random.choice(greetings).format(sender)
    elif message.startswith("!corona"):
        query = message.lower().split(" ", 1)
        if len(query)>1:
            query = query[1]
            if query == "boris johnson":
                return "Happy Hunger Games!"
            else:
                return corona.elaborate_query(query)
    elif message.startswith("!news"):
        query = message.split(" ", 1)
        if len(query)>1:
            news_query = query[1]
            return get_latest_news(news_query)
        else:
            return get_latest_news()
    elif message.startswith("!weather"):
        query = message.split(" ", 1)
        if len(query)>1:
            location = query[1]
            return get_weather(location)
    elif message.startswith("!youtube"):
        query = message.split(" ", 1)
        if len(query)>1:
            return search_youtube_video(query[1])
    elif message.startswith("!tex"):
        query = message.split(" ", 1)
        if len(query)>1:
            return latex_to_text(query[1])
    elif message.startswith("!latex"):
        query = message.split(" ", 1)
        if len(query)>1:
            return latex_to_png(query[1])
    elif message == "!help":
        return '!corona <location> for latest coronavirus report for specified location. \n'\
                    '!news <query> for latest news related to specified query. \n'\
                    '!weather <location> for weather report at specified location. \n'\
                    '!youtube <query> to search for youtube video. \n'\
                    '!latex <query> to compile latex into png. \n'\
                    '!tex <query> to compile latex into unicode.'
    else:
        found_urls = re.findall(r'(https?://[^\s]+)', message)
        for url in found_urls:
            return get_url_info(url)