from lib.apis import get_youtube_videoinfo, search_youtube_video

def register(bot):
    bot.register_command('music', lambda channel, sender, query: search_youtube_video(query, music=True) if query else None)
    bot.register_help('music', '!music <query> to search for music video on youtube.')
