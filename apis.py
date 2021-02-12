import requests
import datetime
from urllib.parse import urlparse, parse_qs, urlencode
from config import *
from utils import json_request, http_request
import pypandoc
from bs4 import BeautifulSoup
import miniflux
import urllib
import emoji

class Chatbot:
    def __init__(self):
        self.context_id = None
        self.last_request_date = datetime.datetime.now()

    def elaborate_query(self, query):

        # if more than one hour after last request, then new context
        time_since_last = (datetime.datetime.now() - self.last_request_date).total_seconds()
        if time_since_last > 3600:
            self.context_id = None
        self.last_request_date = datetime.datetime.now()

        if USE_LOCAL_CHATBOT:
            q = {'key': CHATBOT_KEY, 'input': query}
            if self.context_id:
                q['context'] = self.context_id
            url = 'http://localhost:2834/getreply?' + urlencode(q)
            data = json_request(url, timeout=60)
            if data:
                self.context_id = data["context"]
                return data["output"]

        else:
            q = {'key': CLEVERBOT_KEY, 'input': query}
            if self.context_id:
                q['cs'] = self.context_id
            url = 'https://www.cleverbot.com/getreply?' + urlencode(q)
            data = json_request(url)
            if data:
                self.context_id = data["cs"]
                return data["output"]


class Miniflux:
    def __init__(self):
        self.client = miniflux.Client(MINIFLUX_URL, MINIFLUX_USER, MINIFLUX_PSW)

    def get_new_entries(self, limit = 1):
        try:
            entries = self.client.get_entries(status="unread", limit=limit)["entries"]
        except miniflux.ClientError as err:
            print("miniflux client error: {}".format(err.get_error_reason()), flush=True)
            return None
        except:
            print("Unexpected error getting RSS entries", flush=True)
            return None

        response = ""
        for entry in entries:
            publish_date = datetime.datetime.strptime(entry["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            publish_date = publish_date.strftime("%Y-%m-%d")
            response += "\x0303[miniflux]\x03 {} {} on {} \x02→\x02 {} \n".format(entry["url"], entry["author"], publish_date, entry["title"])
        
        # mark entries as read
        if entries:
            entry_ids = [entry["id"] for entry in entries]
            self.client.update_entries(entry_ids, status="read")

        return response


def get_latest_news(query = None):

    if query:
        url = 'http://newsapi.org/v2/everything?q={}&sortBy=relevancy&apiKey={}'.format(query, NEWSAPI_KEY)
    else:
        url = 'http://newsapi.org/v2/top-headlines?country=it&sortBy=publishedAt&apiKey={}'.format(NEWSAPI_KEY)
        
    data = json_request(url)
    if not data:
        return None
    if data["status"] == "ok" and data["totalResults"] > 0:
        article = data["articles"][0]
        description = article["description"].replace('\n', ' ')
        info = '{} - {}'.format(article["url"], description)
        return info
    else:
        return "I haven't found anything"

def get_weather(location):

    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'.format(location, OPENWEATHER_KEY)
    data = json_request(url)
    if not data:
        return None
    if data["cod"] == '200':
        name = data["city"]["name"]
        today = data["list"][0]

        response = "Weather for {} is {}, the temperature is around {}°C. " \
                    .format(name, today["weather"][0]["description"], today["main"]["temp"])

        for day in data["list"]:
            date = datetime.date.today() + datetime.timedelta(days=1)
            if day["dt_txt"] == date.strftime("%Y-%m-%d 12:00:00"):
                response = response + "Tomorrow at 12:00 will be {}, the temperature will be around {}°C." \
                        .format(day["weather"][0]["description"], day["main"]["temp"])
    else:
        response = data["message"]
    return response

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
    parsed_url = urlparse(query)
    url_queries = parse_qs(parsed_url.query)

    if "v" in url_queries:
        video_id = url_queries["v"][0]
        url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(video_id, YOUTUBE_KEY)
        data = json_request(url)
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
    url = "https://www.googleapis.com/youtube/v3/search?"+urlencode(q)
    data = json_request(url)
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

def search_image(query):
    q = {'num': 1, 'searchType':'image', 'q': query, 'key': YOUTUBE_KEY, 'cx': SEARCH_ENGINE}
    url = "https://www.googleapis.com/customsearch/v1?"+urlencode(q)
    data = json_request(url)
    if not data:
        return None
    items = data["items"]
    if len(items) > 0:
        item = items[0]
        url = item['link']
        title = item['title']
        return f'\x0303[image]\x03 {title} → {url}'

    return "I haven't found anything"

def url_meta(url):
    resp = http_request(url)
    if not resp:
        return None
    soup = BeautifulSoup(resp.text, 'lxml')
    meta = ""
    title = soup.title
    if title:
        title = title.text.strip().replace('\n', ' ')
        meta += f'\x0303<title>\x03 {title} \n'
    description = soup.find('meta', {'name':'description'})
    if not description:
        return meta
    description = description.get('content')
    if not description:
        return meta
    description = description[:200].strip().replace('\n', ' ')
    meta += f'\x0303<description>\x03 {description} \n'
    return meta

def get_url_info(url):
    response = get_youtube_description(url)
    if response:
        return response
    
    response = url_meta(url)
    if response:
        return response


def latex_to_png(formula):
    formula = "\\bg_ffffff {}".format(formula)
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{{300}} {formula}'.format(formula=formula))
    return r.url

def latex_to_text(formula):
    latex = '${}$'.format(formula)
    try:
        return pypandoc.convert_text(latex, 'plain', format='latex')
    except:
        return None

def wolfram_req(query):
    url = f'https://api.wolframalpha.com/v1/result?i={query}&appid={WOLFRAM_KEY}'
    resp = http_request(url)
    if resp:
        return resp.text.replace('\n', '. ')

def plot_function(query):
    q = {'q': query}
    q = urllib.parse.urlencode(q)
    return f'https://frankplus.github.io/plasm?{q}'

def emojize(query):
    return emoji.emojize(query, use_aliases=True)