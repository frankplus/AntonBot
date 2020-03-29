#!/usr/bin/python3

import JustIRC
import random
import corona
import news

channel = "#bugbyte-ita"
botname = "CovidBot"
irc_server_address = "irc.freenode.net"
bot_call_command = "!corona"

corona.irc_formatting = True

bot = JustIRC.IRCConnection()

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup?"
]

def on_connect(bot):
    bot.set_nick(botname)
    bot.send_user_packet(botname)

def on_welcome(bot):
    bot.join_channel(channel)

def on_message(bot, channel, sender, message):
    message = message.strip().lower()
    if message in ["hi", "hello", "yo", "hey"] or botname in message :
        greeting_message = random.choice(greetings).format(sender)
        bot.send_message(channel, greeting_message)
    elif message.startswith(bot_call_command):
        query = message.split(" ", 1)
        if len(query)>1:
            query = query[1]
            if query == "boris johnson":
                bot.send_message(channel, "Happy Hunger Games!")
            else:
                response = corona.elaborate_query(query)
                bot.send_message(channel, response)
    elif message.startswith("!news"):
        query = message.split(" ", 1)
        if len(query)>1:
            news_query = query[1]
            response = news.get_latest_news(news_query)
        else:
            response =  news.get_latest_news()

        bot.send_message(channel, response)
    elif message == "!help":
        response = "!corona <location> for latest coronavirus report for specified location. \
                    !news <query> for latest news related to specified query."
        bot.send_message(channel, response)

def on_private_message(bot, sender, message):
    on_message(bot, sender, sender, message)


bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
bot.on_private_message.append(on_private_message)

bot.connect(irc_server_address)
bot.run_loop()

