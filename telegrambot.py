#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
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

async def get_photo_url_from_message(message):
    photo_url = None
    if message.photo:
        # Photo is present; get the highest resolution photo
        photo_file = await message.photo[-1].get_file()
        photo_url = photo_file.file_path
    return photo_url

async def message_handler(update: Update, context: CallbackContext):
    message = update.message.text

    # If the photo has a caption, use it as the message
    if not message and update.message.caption:
        message = update.message.caption

    # if the message is a photo or is replying to a message containing a photo
    # get the photo url
    photo_url = None
    if update.message.photo:
        photo_url = await get_photo_url_from_message(update.message)
    elif update.message.reply_to_message and update.message.reply_to_message.photo:
        photo_url = await get_photo_url_from_message(update.message.reply_to_message)


    is_private_chat = update.effective_chat.type == 'private'
    is_reply_to_bot = (update.message.reply_to_message is not None and
                       update.message.reply_to_message.from_user.id == context.bot.id)

    # Check if the bot was pinged or if it's a private chat
    bot_pinged = message and \
        ((context.bot.username in message) or \
         (context.bot.first_name in message)) or \
         any(word in message for word in config.ALT_NAMES) or \
         is_private_chat or is_reply_to_bot

    chat_id = str(update.effective_chat.id)
    bot_instance = bot.get_bot_instance(chat_id)

    if update.message.from_user.username:
        sender = '@'+update.message.from_user.username
    else:
        sender = update.message.from_user.first_name
        
    # Add the message to the conversation history
    bot_instance.last_conversation_lines.append(f"{sender}: {message}")
    while len(bot_instance.last_conversation_lines) > 50:
        bot_instance.last_conversation_lines.pop(0)

    if bot_pinged or (config.AUTO_SPEAK and random.random() < config.AUTO_SPEAK_PROBABILITY):
        answer = bot_instance.chatbot.elaborate_query(bot_instance.last_conversation_lines, photo_url)
        if not answer: return None
        bot_instance.last_conversation_lines.append(f"{config.BOTNAME}: {answer}")
        await update.message.reply_text(answer)


def main(blocking = True):
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    for command, handler in bot.handlers.items():
        def make_handler(handler):
            async def telegram_handler(update: Update, context: CallbackContext):
                chat_id = str(update.effective_chat.id)
                if update.message.from_user.username:
                    from_user = '@'+update.message.from_user.username
                else:
                    from_user = update.message.from_user.first_name
                arg = " ".join(context.args)
                response = handler(chat_id, from_user, arg)
                await update.message.reply_text(response)
            return telegram_handler

        application.add_handler(CommandHandler(command, make_handler(handler)))

    # On non-command i.e message 
    application.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & (~filters.COMMAND), message_handler))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()
