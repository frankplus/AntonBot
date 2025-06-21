from lib.apis import *
import re
import random
from config import BOTNAME
import config
import os
import importlib
import logging

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

class BotInstance:
    def __init__(self, id, plugin_bot=None):
        self.id = id
        self.chatbot = Chatbot(plugin_bot)
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

class PluginBot:
    def __init__(self):
        self.handlers = {}
        self.help_entries = {}
        self.bot_instances = dict()
        # Function calling support
        self.available_functions = {}
        self.function_definitions = []
        self.load_plugins()
        # Register built-in commands
        self.register_builtin_commands()

    def register_command(self, name, handler):
        self.handlers[name] = handler

    def register_help(self, name, help_text):
        self.help_entries[name] = help_text

    def register_function(self, function_handler, function_definition):
        """Register a function for OpenAI function calling"""
        function_name = function_definition.get("name")
        if function_name:
            self.available_functions[function_name] = function_handler
            self.function_definitions.append(function_definition)
            logging.info(f"Registered function: {function_name}")
        else:
            logging.warning("Function definition missing 'name' field")

    def get_function_definitions(self):
        """Get all registered function definitions"""
        return self.function_definitions

    def get_available_functions(self):
        """Get all available function handlers"""
        return self.available_functions

    def get_help(self, channel, sender, query):
        if query:
            return self.help_entries.get(query, "Invalid command")
        else:
            return "COMMANDS: {} \nSee !help <command> for details".format(" ".join(self.help_entries.keys()))

    def get_bot_instance(self, id):
        if id not in self.bot_instances:
            self.bot_instances[id] = BotInstance(id, self)
        return self.bot_instances[id]

    def load_plugins(self):
        plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        if not os.path.isdir(plugins_dir):
            return
        for name in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, name)
            if os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, '__init__.py')):
                try:
                    module = importlib.import_module(f'plugins.{name}')
                    if hasattr(module, 'register'):
                        module.register(self)
                except Exception as e:
                    print(f"Failed to load plugin {name}: {e}")

    def register_builtin_commands(self):
        self.register_command('help', lambda channel, sender, query: self.get_help(channel, sender, query))
        pass

plugin_bot = PluginBot()

async def elaborate_query(channel, sender, message):
    message = message.strip()
    if not message: return None
    if message.startswith("!"):
        splitted = message[1:].split(" ", 1)
        command = splitted[0]
        args = splitted[1] if len(splitted)>1 else ""
        if command in plugin_bot.handlers:
            return plugin_bot.handlers[command](channel, sender, args)
    elif message.lower() in ["hi", "hello", "yo", "hey", "we"]:
        return random.choice(greetings).format(sender)
    elif enableUrlInfo:
        found_urls = re.findall(r'(https?://[^\s]+)', message)
        for url in found_urls:
            info = get_url_info(url)
            if info:
                return info
    pos = message.find(BOTNAME)
    bot_pinged = True if pos != -1 else False
    bot_instance = plugin_bot.get_bot_instance(channel)
    bot_instance.last_conversation_lines.append(f"{sender}: {message}")
    while len(bot_instance.last_conversation_lines) > 50:
        bot_instance.last_conversation_lines.pop(0)
    if bot_pinged or (config.AUTO_SPEAK and random.random() < AUTO_SPEAK_PROBABILITY):
        answer = bot_instance.chatbot.elaborate_query(bot_instance.last_conversation_lines)
        if not answer: return None
        bot_instance.last_conversation_lines.append(f"{BOTNAME}: {answer}")
        return answer

def on_join(sender, channel):
    sender = str(sender)
    if sender == BOTNAME:
        return "Hey y'all. Who summoned me?"
    return plugin_bot.get_bot_instance(channel).on_join(sender)
