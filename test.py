#!/usr/bin/python3

import sys
import corona 
import bot

while True:
    print('Input: ')
    query = input()
    print(bot.elaborate_query("channel_test", "MrFrank", query))