#!/usr/bin/python3

"""
    Starts both the IRC and the telegram bot
"""

import ircbot
import telegrambot
import threading

ircbot_thread = threading.Thread(target=ircbot.main, daemon=True)
ircbot_thread.start()

telegrambot.main()

ircbot_thread.join()