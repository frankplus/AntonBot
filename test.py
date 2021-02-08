#!/usr/bin/python3


import bot
import asyncio

async def main():
    while True:
        print('Input: ')
        query = input()
        response = await bot.elaborate_query("channel_test", "MrFrank", query)
        print(response)

asyncio.run(main())