from lib.apis import *
import re
import random
from lib import corona, game, chessbot
from config import BOTNAME
import config

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
        'plot': '!plot <query> to plot any mathematical function.',
        'tweet': '!tweet <message> to tweet a message',
        'fortune': '!fortune try this command yourself ;)',
        'shush': '!shush to make me stop being annoying',
        'talk': '!talk if you want me to participate in your conversations',
        'tell': '!tell <recipient> <message> to tell a message when the recipient joins the channel'
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
        self.tell_on_join = dict()
    
    def add_tell(self, query):
        splitted = query.split(" ", 1)
        recipient = splitted[0]
        message = splitted[1] if len(splitted)>1 else ""
        self.tell_on_join[recipient] = message
        return "sure"
    
    def on_join(self, joiner):
        if joiner in self.tell_on_join:
            message = self.tell_on_join[joiner]
            del self.tell_on_join[joiner]
            return f"{joiner}, {message}"

bot_instances = dict()

def get_bot_instance(id):
    global bot_instances
    if id not in bot_instances:
        bot_instances[id] = BotInstance(id)
    return bot_instances[id]

def set_bot_autospeak(autospeak):
    config.AUTO_SPEAK = autospeak
    if autospeak:
        return "I will join your conversations"
    else:
        return "I'll be quiet then"

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
    "tweet": lambda channel, sender, query: tweet(query),
    "fortune": lambda channel, sender, query: fortune(),
    "shush": lambda channel, sender, query: set_bot_autospeak(False),
    "talk": lambda channel, sender, query: set_bot_autospeak(True),
    "tell": lambda channel, sender, query: get_bot_instance(channel).add_tell(query) if query else None,
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

    bot_instance = get_bot_instance(channel)
    bot_instance.last_conversation_lines.append({"role": "user", "content": message})
    while len(bot_instance.last_conversation_lines) > 5:
        bot_instance.last_conversation_lines.pop(0)

    if bot_pinged or (config.AUTO_SPEAK and random.random() < AUTO_SPEAK_PROBABILITY):
        answer = bot_instance.chatbot.elaborate_query(bot_instance.last_conversation_lines)
        if not answer: return None
        bot_instance.last_conversation_lines.append({"role": "assistant", "content": answer})
        return answer


def on_join(sender, channel):
    sender = str(sender)
    if sender == BOTNAME:
        return "Hey y'all. Who summoned me?"

    return get_bot_instance(channel).on_join(sender)
