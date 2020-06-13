from apis import *
import re
import random
import corona
import game
from config import BOTNAME
import game_akinator

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup?"
]

game_instance = game.Game()
cleverbot = Cleverbot()

def elaborate_query(sender, message):
    message = message.strip()
    if message.startswith("!corona"):
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
    elif message.startswith("!image"):
        query = message.split(" ", 1)
        if len(query)>1:
            return search_image(query[1])
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
            return game_instance.elaborate_query(sender, query[1])
        else:
            return game_instance.elaborate_query(sender, "")
    elif message.startswith("!wolfram"):
        query = message.split(" ", 1)
        if len(query)>1:
            return wolfram_req(query[1])
    elif message.startswith("!plot"):
        query = message.split(" ", 1)
        if len(query)>1:
            return plot_function(query[1])
    elif message.startswith("!akinator"):
        query = message.split(" ", 1)
        if len(query)>1:
            return game_akinator.elaborate_query(query[1])
    elif message[0] == ':' and message[-1] == ':' and len(message) >= 3:
        return emojize(message)
    elif message.startswith("!help"):
        commands = {
            'corona': '!corona <location> for latest coronavirus report for specified location.',
            'news': '!news <query> for latest news related to specified query.',
            'weather': '!weather <location> for weather report at specified location.',
            'youtube': '!youtube <query> to search for youtube video.',
            'image': '!image <query> to search for an image.',
            'latex': '!latex <query> to compile latex into png.',
            'tex': '!tex <query> to compile latex into unicode.',
            'music': '!music <query> to search for music video on youtube.',
            'game': game.get_help(),
            'wolfram': '!wolfram <query> to calculate or ask any question.',
            'plot': '!plot <query> to plot any mathematical function.',
            'die': '!die to kill the bot.'
        }
        query = message.split(" ", 1)
        if len(query)>1:
            return commands.get(query[1], "Invalid command")
        else:
            return "COMMANDS: {} \nSee !help <command> for details".format(" ".join(commands.keys()))
    elif message.lower() in ["hi", "hello", "yo", "hey"]:
        return random.choice(greetings).format(sender)
    elif message == "!die" :
        exit(1)
    else:
        found_urls = re.findall(r'(https?://[^\s]+)', message)
        for url in found_urls:
            info = get_url_info(url)
            if info:
                return info

    # cleverbot
    pos = message.find(BOTNAME)
    if pos != -1:
        if pos == 0:
            split = message.split(' ', 1)
            if len(split) > 1:
                message = split[1]
        else:
            message = message.replace(BOTNAME, ' ')
        return cleverbot.elaborate_query(message)