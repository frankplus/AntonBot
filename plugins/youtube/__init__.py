from lib.utils import json_request_get
import urllib
import datetime
from config import YOUTUBE_KEY

def get_youtube_videoinfo(item):
    title = item["snippet"]["title"]
    channel = item["snippet"]["channelTitle"]
    description = item["snippet"]["description"]
    description = description[:150] if len(description) > 150 else description
    description = description.replace('\n', ' ')
    publish_date = item["snippet"]["publishedAt"]
    try:
        publish_date = datetime.datetime.strptime(item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S.%f%z")
    except :
        publish_date = datetime.datetime.strptime(item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S%z")
    publish_date = publish_date.strftime("%b %d %Y")
    return "{} on {} \x02{} →\x02 {}".format(channel, publish_date, title, description)

def get_youtube_description(query):
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(query)
    url_queries = parse_qs(parsed_url.query)
    if "v" in url_queries:
        video_id = url_queries["v"][0]
        url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(video_id, YOUTUBE_KEY)
        data = json_request_get(url)
        if not data:
            return None
        items = data["items"]
        if len(items) > 0:
            info = get_youtube_videoinfo(items[0])
            return "\x0303[youtube]\x03 {}".format(info)

def search_youtube_video(query, music=False):
    q = {'part':'snippet', 'maxResults': 1, 'type':'video', 'q': query, 'key': YOUTUBE_KEY}
    if music:
        q['videoCategoryId'] = 10
    url = "https://www.googleapis.com/youtube/v3/search?"+urllib.parse.urlencode(q)
    data = json_request_get(url)
    if not data:
        return None
    items = data["items"]
    if len(items) > 0:
        item = items[0]
        video_id = item["id"]["videoId"]
        url = "https://www.youtube.com/watch?v={}".format(video_id)
        info = get_youtube_videoinfo(item)
        return "\x0303[youtube]\x03 {} {}".format(url, info)
    return "I haven't found anything"

def register(bot):
    bot.register_command('youtube', lambda channel, sender, query: search_youtube_video(query) if query else None)
    bot.register_help('youtube', '!youtube <query> to search for youtube video.')
