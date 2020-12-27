from apis import *
import re
import random
import corona
import game
import chessbot
from config import BOTNAME

enableUrlInfo = True

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup {}?",
    "yo {}!",
    "we {}!"
]

game_instance = game.Game()
cleverbot = Cleverbot()
chess_instance = chessbot.Game()

def get_help(sender, query):
    commands = {
        'corona': '!corona <location> for latest coronavirus report for specified location.',
        'news': '!news <query> for latest news related to specified query.',
        'weather': '!weather <location> for weather report at specified location.',
        'youtube': '!youtube <query> to search for youtube video.',
        'image': '!image <query> to search for an image.',
        'music': '!music <query> to search for music video on youtube.',
        'latex': '!latex <query> to compile latex into png.',
        'tex': '!tex <query> to compile latex into unicode.',
        'game': game.get_help(),
        'chess': chessbot.get_help(),
        'wolfram': '!wolfram <query> to calculate or ask any question.',
        'plot': '!plot <query> to plot any mathematical function.',
        'die': '!die to kill the bot.'
    }
    if query:
        return commands.get(query, "Invalid command")
    else:
        return "COMMANDS: {} \nSee !help <command> for details".format(" ".join(commands.keys()))

handlers = {
    "corona": lambda sender, query: corona.elaborate_query(query) if query else None,
    "news": lambda sender, query: get_latest_news(query),
    "weather": lambda sender, query: get_weather(query) if query else None,
    "youtube": lambda sender, query: search_youtube_video(query) if query else None,
    "image": lambda sender, query: search_image(query) if query else None,
    "music": lambda sender, query: search_youtube_video(query, music = True) if query else None,
    "tex": lambda sender, query: latex_to_text(query) if query else None,
    "latex": lambda sender, query: latex_to_png(query) if query else None,
    "game": lambda sender, query: game_instance.elaborate_query(sender, query),
    "chess": lambda sender, query: chess_instance.elaborate_query(sender, query),
    "wolfram": lambda sender, query: wolfram_req(query) if query else None,
    "plot": lambda sender, query: plot_function(query) if query else None,
    "help": get_help,
    "die": lambda sender, query: exit(1),
}

def elaborate_query(sender, message):
    message = message.strip()

    if message.startswith("!"):
        splitted = message[1:].split(" ", 1)
        command = splitted[0]
        param = splitted[1] if len(splitted)>1 else ""
        if command in handlers:
            return handlers[command](sender, param)

    elif message[0] == ':' and message[-1] == ':' and len(message) >= 3:
        return emojize(message)
    elif message.lower() in ["hi", "hello", "yo", "hey", "we"]:
        return random.choice(greetings).format(sender)
    elif enableUrlInfo:
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


def on_join(sender):
    if sender == BOTNAME:
        return "Hey y'all. Mr Bot is here!"

    if sender == "MrFrank":
        return "MrFrank sito inseminio?"