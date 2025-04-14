def register(bot):
    bot.register_command('image', lambda channel, sender, query: bot.get_bot_instance(channel).chatbot.generate_image(query) if query else None)
    bot.register_help('image', '!image <prompt> to generate an image.')
