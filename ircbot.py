#!/usr/bin/python3

import JustIRC
import bot
import threading
from timeloop import Timeloop
from datetime import timedelta
from config import CHANNEL, BOTNAME, IRC_SERVER_ADDRESS
import config
from apis import Miniflux

conn = JustIRC.IRCConnection()

@conn.on("connect")
def on_connect(e):
    conn.set_nick(BOTNAME)
    conn.send_user_packet(BOTNAME)

@conn.on("welcome")
def on_welcome(e):
    conn.join_channel(CHANNEL)

@conn.on("message")
def on_message(e):
    with open("chatlog.txt", 'a+') as f:
        f.write(f"{e.sender}: {e.message}\n")
    channel = e.channel if e.channel != BOTNAME else e.sender # check private message
    response = bot.elaborate_query(channel, e.sender, e.message)
    if response:
        lines = response.split("\n")
        for line in lines:
            conn.send_message(channel, line)

@conn.on("join")
def on_join(e):
    response = bot.on_join(e.nick)
    if response:
        conn.send_message(e.channel, response)


def main():
    conn.connect(IRC_SERVER_ADDRESS)
    print("IRC bot connected", flush=True)

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