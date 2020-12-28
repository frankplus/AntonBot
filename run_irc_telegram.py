#!/usr/bin/python3

"""
    Starts both the IRC and the telegram bot
"""

import ircbot
import telegrambot

telegrambot.main(blocking = False)
ircbot.main()