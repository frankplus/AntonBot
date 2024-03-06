#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters
import bot
from lib import corona
import config
import random

corona.irc_formatting = False

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def error_handler(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def message_handler(update: Update, context: CallbackContext):
    message = update.message.text
    bot_pinged = update.message.text and context.bot.username in update.message.text

    chat_id = str(update.effective_chat.id)
    bot_instance = bot.get_bot_instance(chat_id)

    if update.message.from_user.username:
        sender = '@'+update.message.from_user.username
    else:
        sender = update.message.from_user.first_name
        
    bot_instance.last_conversation_lines.append(f"{sender}: {message}")
    while len(bot_instance.last_conversation_lines) > 50:
        bot_instance.last_conversation_lines.pop(0)

    if bot_pinged or (config.AUTO_SPEAK and random.random() < config.AUTO_SPEAK_PROBABILITY):
        answer = bot_instance.chatbot.elaborate_query(bot_instance.last_conversation_lines)
        if not answer: return None
        bot_instance.last_conversation_lines.append(f"{config.BOTNAME}: {answer}")
        update.message.reply_text(answer)


def main(blocking = True):
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
                chat_id = str(update.effective_chat.id)
                if update.message.from_user.username:
                    from_user = '@'+update.message.from_user.username
                else:
                    from_user = update.message.from_user.first_name
                arg = " ".join(context.args)
                response = handler(chat_id, from_user, arg)
                update.message.reply_text(response)
            return telegram_handler

        dispatcher.add_handler(CommandHandler(command, make_handler(handler)))

    # On non-command i.e message 
    dispatcher.add_handler(MessageHandler(filters.text & (~filters.command), message_handler))

    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    if blocking:
        updater.idle()


if __name__ == '__main__':
    main()
