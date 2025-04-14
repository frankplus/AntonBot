from lib.apis import search_youtube_video

def register(bot):
    bot.register_command('youtube', lambda channel, sender, query: search_youtube_video(query) if query else None)
    bot.register_help('youtube', '!youtube <query> to search for youtube video.')
