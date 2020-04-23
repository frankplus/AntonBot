#!/usr/bin/python3

import JustIRC
import bot
import threading
import minifluxapi as rss
from timeloop import Timeloop
from datetime import timedelta
from utils import channel, botname, irc_server_address

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

# rss feed
rss_thread = Timeloop()

@rss_thread.job(interval=timedelta(seconds=60))
def send_rss_updates():
    response = rss.get_new_entries()
    if response:
        lines = response.split("\n")
        for line in lines:
            conn.send_message(channel, line)

# connect
conn.on_connect.append(on_connect)
conn.on_welcome.append(on_welcome)
conn.on_public_message.append(on_message)
conn.on_private_message.append(on_private_message)

conn.connect(irc_server_address)

rss_thread.start()
conn.run_loop()

