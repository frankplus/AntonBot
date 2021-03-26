from apis import *
import re
import random
import corona
import game
import chessbot
from config import BOTNAME
import iliad
import config
import datetime

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

def get_help(channel, sender, query):
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
        'plot': '!plot <query> to plot any mathematical function.'
    }
    if query:
        return commands.get(query, "Invalid command")
    else:
        return "COMMANDS: {} \nSee !help <command> for details".format(" ".join(commands.keys()))

class BotInstance:
    def __init__(self, id):
        self.id = id
        self.game_instance = game.Game()
        self.chatbot = Chatbot()
        self.chess_instance = chessbot.Game(id)
        self.last_conversation_lines = list()

bot_instances = dict()

def get_bot_instance(id):
    global bot_instances
    if id not in bot_instances:
        bot_instances[id] = BotInstance(id)
    return bot_instances[id]


handlers = {
    "corona": lambda channel, sender, query: corona.elaborate_query(query) if query else None,
    "news": lambda channel, sender, query: get_latest_news(query),
    "weather": lambda channel, sender, query: get_weather(query) if query else None,
    "youtube": lambda channel, sender, query: search_youtube_video(query) if query else None,
    "image": lambda channel, sender, query: search_image(query) if query else None,
    "music": lambda channel, sender, query: search_youtube_video(query, music = True) if query else None,
    "tex": lambda channel, sender, query: latex_to_text(query) if query else None,
    "latex": lambda channel, sender, query: latex_to_png(query) if query else None,
    "game": lambda channel, sender, query: get_bot_instance(channel).game_instance.elaborate_query(sender, query),
    "chess": lambda channel, sender, query: get_bot_instance(channel).chess_instance.elaborate_query(sender, query),
    "wolfram": lambda channel, sender, query: wolfram_req(query) if query else None,
    "plot": lambda channel, sender, query: plot_function(query) if query else None,
    "iliad": lambda channel, sender, query: f"Dati rimanenti giornalieri: {iliad.totale_dati_giornalieri(config.iliad_login_info):.2f} GB",
    "help": get_help
}

async def elaborate_query(channel, sender, message):
    message = message.strip()

    if message.startswith("!"):
        splitted = message[1:].split(" ", 1)
        command = splitted[0]
        args = splitted[1] if len(splitted)>1 else ""
        if command in handlers:
            return handlers[command](channel, sender, args)

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

    # chatbot pinged
    pos = message.find(BOTNAME)
    bot_pinged = True if pos != -1 else False

    if bot_pinged:
        # remove bot name
        if pos == 0:
            split = message.split(' ', 1)
            if len(split) > 1:
                message = split[1]
        else:
            message = message.replace(BOTNAME, ' ')

    bot_instance = get_bot_instance(channel)
    bot_instance.last_conversation_lines.append(message)
    while len(bot_instance.last_conversation_lines) > 5:
        bot_instance.last_conversation_lines.pop(0)


    if bot_pinged or (config.AUTO_SPEAK and random.random() < AUTO_SPEAK_PROBABILITY):
        context = "\n".join(bot_instance.last_conversation_lines)
        answer, score = bot_instance.chatbot.elaborate_query(context, new_context=True)
        if bot_pinged or (random.random() < pow(2, 0.3*score)):
            return answer




def on_join(sender):
    if sender == BOTNAME:
        return "Hey y'all. Who summoned me?"