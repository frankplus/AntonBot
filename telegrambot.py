#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, PrefixHandler, Filters, CallbackContext
import bot
import corona
import config

corona.irc_formatting = False
bot.enableUrlInfo = False

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def on_message(update: Update, context: CallbackContext) -> None:
    """reply the user message."""
    response = bot.elaborate_query(update.message.from_user.first_name, update.message.text)
    print(update.message.text)
    if response:
        lines = response.split("\n")
        for line in lines:
            update.message.reply_text(line)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    for command, handler in bot.handlers.items():
        def make_handler(handler):
            def telegram_handler(update: Update, context: CallbackContext):
                from_user = update.message.from_user.first_name
                arg = " ".join(context.args)
                response = handler(from_user, arg)
                update.message.reply_text(response)
            return telegram_handler

        dispatcher.add_handler(PrefixHandler(['!', '#', '/'], command, make_handler(handler)))

    # on noncommand i.e message 
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, on_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()