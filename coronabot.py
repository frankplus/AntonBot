#!/usr/bin/python3

import JustIRC
import apis

channel = "#bugbyte-ita"
botname = "CovidBot"
irc_server_address = "irc.freenode.net"

bot = JustIRC.IRCConnection()

def on_connect(bot):
    bot.set_nick(botname)
    bot.send_user_packet(botname)

def on_welcome(bot):
    bot.join_channel(channel)

def on_message(bot, channel, sender, message):
    response = apis.elaborate_query(sender, message)
    lines = response.split("\n")
    for line in lines:
        bot.send_message(channel, line)

def on_private_message(bot, sender, message):
    response = apis.elaborate_query(sender, message)
    lines = response.split("\n")
    for line in lines:
        bot.send_message(channel, line)


bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
bot.on_private_message.append(on_private_message)

bot.connect(irc_server_address)
bot.run_loop()

