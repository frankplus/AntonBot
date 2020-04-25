#!/usr/bin/python3

import JustIRC
import bot
import threading
from timeloop import Timeloop
from datetime import timedelta
from config import CHANNEL, BOTNAME, IRC_SERVER_ADDRESS
from apis import Miniflux

conn = JustIRC.IRCConnection()

def on_connect(conn):
    conn.set_nick(BOTNAME)
    conn.send_user_packet(BOTNAME)

def on_welcome(conn):
    conn.join_channel(CHANNEL)

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
rss = Miniflux()

@rss_thread.job(interval=timedelta(seconds=60))
def send_rss_updates():
    response = rss.get_new_entries()
    if response:
        lines = response.split("\n")
        for line in lines:
            conn.send_message(CHANNEL, line)

# connect
conn.on_connect.append(on_connect)
conn.on_welcome.append(on_welcome)
conn.on_public_message.append(on_message)
conn.on_private_message.append(on_private_message)

conn.connect(IRC_SERVER_ADDRESS)

# run
rss_thread.start()
conn.run_loop()

