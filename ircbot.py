#!/usr/bin/python3

from pyrcb2 import IRCBot, Event
import bot
import threading
from timeloop import Timeloop
from datetime import timedelta
from config import CHANNEL, BOTNAME, IRC_SERVER_ADDRESS
import config
from apis import Miniflux
import asyncio

class MyBot:
    def __init__(self):
        self.bot = IRCBot(log_communication=True)
        self.bot.load_events(self)

    def start(self):
        self.bot.call_coroutine(self.start_async())

    async def start_async(self):
        await self.bot.connect(IRC_SERVER_ADDRESS, 6667)
        await self.bot.register(BOTNAME)
        await self.bot.join(CHANNEL)
        self.bot.schedule_coroutine(self.rss_reader_loop())
        await self.bot.listen()

    @Event.privmsg
    def on_privmsg(self, sender, channel, message):
        if channel is None:
            channel = sender

        with open("chatlog.txt", 'a+') as f:
            f.write(f"{sender}: {message}\n")
        response = bot.elaborate_query(channel, sender, message)
        if response:
            lines = response.split("\n")
            for line in lines:
                if line:
                    self.bot.privmsg(channel, line)

    @Event.join
    async def on_join(self, sender, channel):
        response = bot.on_join(sender)
        if response:
            self.bot.privmsg(channel, response)

    async def rss_reader_loop(self):
        rss = Miniflux()
        while True:
            response = rss.get_new_entries()
            if response:
                lines = response.split("\n")
                for channel in self.bot.channels:
                    for line in lines:
                        if line: 
                            self.bot.privmsg(channel, line)
            await asyncio.sleep(60)


def main():
    mybot = MyBot()
    mybot.start()
    print("IRC bot connected", flush=True)


if __name__ == '__main__':
    main()