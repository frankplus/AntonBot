#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, PrefixHandler, CallbackContext, MessageHandler, Filters
import bot
import corona
import config

corona.irc_formatting = False

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def mention_handler(update: Update, context: CallbackContext):
    text = update.message.text
    new_text = text
    mentioned = False

    for entity in update.message.entities:
        if entity.type == "mention":
            mention = text[entity.offset : entity.offset+entity.length]
            user_mentioned = mention[1:]
            if user_mentioned == context.bot.username:
                mentioned = True
            new_text = new_text.replace(mention, "")
    
    if mentioned:
        chat_id = str(update.effective_chat.id)
        response = bot.get_bot_instance(chat_id).cleverbot.elaborate_query(new_text.strip())
        update.message.reply_text(response)


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

        dispatcher.add_handler(PrefixHandler(['!', '#', '/'], command, make_handler(handler)))

    dispatcher.add_handler(MessageHandler(Filters.entity("mention"), mention_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    if blocking:
        updater.idle()


if __name__ == '__main__':
    main()