#!/usr/bin/python3

from pyrcb2 import IRCBot, Event
import bot
from config import CHANNEL, BOTNAME, IRC_SERVER_ADDRESS, IRC_SERVER_PASS
import asyncio
import logging

logging.basicConfig(filename='bot_log.txt', level=logging.INFO)

class MyBot:
    def __init__(self):
        self.bot = IRCBot(log_communication=True)
        self.bot.load_events(self)

    async def run(self):
        async def init():
            await self.bot.connect(IRC_SERVER_ADDRESS, 6667)
            if IRC_SERVER_PASS: await self.bot.send_command("PASS", IRC_SERVER_PASS)
            await self.bot.register(BOTNAME)
            await self.bot.join(CHANNEL)
            logging.info("IRC bot connected")
        await self.bot.run(init())

    @Event.privmsg
    async def on_privmsg(self, sender, channel, message):
        if channel is None:
            channel = sender

        with open("chatlog.txt", 'a+') as f:
            f.write(f"{sender}: {message}\n")

        try:
            response = await bot.elaborate_query(channel, sender, message)
            if response:
                lines = response.split("\n")
                for line in lines:
                    if line:
                        self.bot.privmsg(channel, line)
        except:
            logging.exception(f'An exception was thrown while elaborating message: {message}')

    @Event.join
    async def on_join(self, sender, channel):
        response = bot.on_join(sender, channel)
        if response:
            self.bot.privmsg(channel, response)


async def main():
    mybot = MyBot()
    await mybot.run()


if __name__ == '__main__':
    asyncio.run(main())
