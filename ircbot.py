#!/usr/bin/python3

import JustIRC
import bot
import threading
from timeloop import Timeloop
from datetime import timedelta
from config import CHANNEL, BOTNAME, IRC_SERVER_ADDRESS
import config
from apis import Miniflux

def on_connect(conn):
    conn.set_nick(BOTNAME)
    conn.send_user_packet(BOTNAME)

def on_welcome(conn):
    conn.join_channel(CHANNEL)
    conn.join_channel("#bugbyte-game")

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

def on_join(conn, channel, sender):
    response = bot.on_join(sender)
    if response:
        conn.send_message(channel, response)


def main():
    conn = JustIRC.IRCConnection()

    # connect
    conn.on_connect.append(on_connect)
    conn.on_welcome.append(on_welcome)
    conn.on_public_message.append(on_message)
    conn.on_private_message.append(on_private_message)
    conn.on_join.append(on_join)

    conn.connect(IRC_SERVER_ADDRESS)

    # run
    if config.ENABLE_MINIFLUX:
        rss_thread = Timeloop()
        rss = Miniflux()

        @rss_thread.job(interval=timedelta(seconds=300))
        def send_rss_updates(rss=rss):
            response = rss.get_new_entries()
            if response:
                lines = response.split("\n")
                for line in lines:
                    conn.send_message(CHANNEL, line)

        rss_thread.start()

    conn.run_loop()

if __name__ == '__main__':
    main()