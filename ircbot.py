#!/usr/bin/python3

import JustIRC
import bot

channel = "#bugbyte-ita"
botname = "CovidBot"
irc_server_address = "irc.freenode.net"

conn = JustIRC.IRCConnection()

def on_connect(conn):
    conn.set_nick(botname)
    conn.send_user_packet(botname)

def on_welcome(conn):
    conn.join_channel(channel)

def on_message(conn, channel, sender, message):
    response = bot.elaborate_query(sender, message)
    if response:
        lines = response.split("\n")
        for line in lines:
            conn.send_message(channel, line)

def on_private_message(conn, sender, message):
    response = bot.elaborate_query(sender, message)
    if response:
        lines = response.split("\n")
        for line in lines:
            conn.send_message(sender, line)


conn.on_connect.append(on_connect)
conn.on_welcome.append(on_welcome)
conn.on_public_message.append(on_message)
conn.on_private_message.append(on_private_message)

conn.connect(irc_server_address)
conn.run_loop()

