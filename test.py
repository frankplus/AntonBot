#!/usr/bin/python3

import sys
import corona 
import bot

while True:
    query = input()
    print(bot.elaborate_query("MrFrank", query))