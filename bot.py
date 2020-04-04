from apis import *
import random
import corona
import game

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup?"
]

game_instance = game.Game()

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
    elif message.startswith("!music"):
        query = message.split(" ", 1)
        if len(query)>1:
            return search_youtube_video(query[1], music = True)
    elif message.startswith("!tex"):
        query = message.split(" ", 1)
        if len(query)>1:
            return latex_to_text(query[1])
    elif message.startswith("!latex"):
        query = message.split(" ", 1)
        if len(query)>1:
            return latex_to_png(query[1])
    elif message.startswith("!game"):
        query = message.split(" ", 1)
        global game_instance
        if len(query)>1:
            return game_instance.elaborate_query(query[1])
        else:
            return game_instance.elaborate_query("")
    elif message.startswith("!help"):
        commands = {
            'corona': '!corona <location> for latest coronavirus report for specified location.',
            'news': '!news <query> for latest news related to specified query.',
            'weather': '!weather <location> for weather report at specified location.',
            'youtube': '!youtube <query> to search for youtube video.',
            'latex': '!latex <query> to compile latex into png.',
            'tex': '!tex <query> to compile latex into unicode.',
            'music': '!music <query> to search for music video on youtube.',
            'game': game.get_help()
        }
        query = message.split(" ", 1)
        if len(query)>1:
            return commands.get(query[1], "Invalid command")
        else:
            return "COMMANDS: {} \nSee !help <command> for details".format(" ".join(commands.keys()))

    else:
        found_urls = re.findall(r'(https?://[^\s]+)', message)
        for url in found_urls:
            info = get_url_info(url)
            if info:
                return info