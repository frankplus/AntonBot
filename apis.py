import requests
import random
import corona
import datetime
import re
from urllib.parse import urlparse, parse_qs
from apikeys import *
from pylatexenc.latex2text import LatexNodes2Text


greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup?"
]

def get_latest_news(query = None):

    if query:
        url = 'http://newsapi.org/v2/everything?q={}&sortBy=relevancy&apiKey={}'.format(query, newsapi_key)
    else:
        url = 'http://newsapi.org/v2/top-headlines?country=it&sortBy=publishedAt&apiKey={}'.format(newsapi_key)
        
    r = requests.get(url)
    data = r.json()
    if data["status"] == "ok" and data["totalResults"] > 0:
        article = data["articles"][0]
        info = '{} - {}'.format(article["url"], article["description"])
        return info
    else:
        return "I haven't found anything"

def get_weather(location):

    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'.format(location, openweather_key)
    data = requests.get(url).json()
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

def get_youtube_description(query):
    parsed_url = urlparse(query)
    url_queries = parse_qs(parsed_url.query)

    if "v" in url_queries:
        video_id = url_queries["v"][0]
        url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(video_id, youtube_key)
        data = requests.get(url).json()
        items = data["items"]
        if len(items) > 0:
            title = items[0]["snippet"]["title"]
            description = items[0]["snippet"]["description"]
            description = description[:150] if len(description) > 150 else description
            parsed_url = parsed_url._replace(netloc='invidio.us') # replace youtube into invidio.us
            invidio_url = parsed_url.geturl()
            return "{} {} - {}".format(invidio_url, title, description)
    

def search_youtube_video(query):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q={}&maxResults=1&type=video&key={}".format(query, youtube_key)
    data = requests.get(url).json()
    items = data["items"]
    if len(items) > 0:
        item = items[0]
        video_id = item["id"]["videoId"]
        url = "https://www.invidio.us/watch?v={}".format(video_id)
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        description = description[:150] if len(description) > 150 else description
        return "{} {} - {}".format(url, title, description)

def url_meta(url):
    req_url = "https://api.urlmeta.org/?url={}".format(url)
    data = requests.get(req_url, headers={'Authorization': urlmeta_api_authorization}).json()
    if data["result"]["status"] == "OK":
        title = data["meta"]["title"]
        if "description" in data["meta"]:
            description = data["meta"]["description"]
            description = description[:200] if len(description) > 200 else description
            return "{} - {}".format(title, description)
        return title

def get_url_info(url):
    # check if youtube url
    response = get_youtube_description(url)
    if response:
        return response
    
    # get url meta informations
    response = url_meta(url)
    if response:
        return response

    return ""


def latex_to_png(formula):
    formula = "\\bg_ffffff {}".format(formula)
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{{300}} {formula}'.format(formula=formula))
    return r.url

def latex_to_text(formula):
    return LatexNodes2Text().latex_to_text(formula)


def elaborate_query(sender, message):
    message = message.strip()
    if message.lower() in ["hi", "hello", "yo", "hey"]:
        return random.choice(greetings).format(sender)
    elif message.startswith("!corona"):
        query = message.lower().split(" ", 1)
        if len(query)>1:
            query = query[1]
            if query == "boris johnson":
                return "Happy Hunger Games!"
            else:
                return corona.elaborate_query(query)
    elif message.startswith("!news"):
        query = message.split(" ", 1)
        if len(query)>1:
            news_query = query[1]
            return get_latest_news(news_query)
        else:
            return get_latest_news()
    elif message.startswith("!weather"):
        query = message.split(" ", 1)
        if len(query)>1:
            location = query[1]
            return get_weather(location)
    elif message.startswith("!youtube"):
        query = message.split(" ", 1)
        if len(query)>1:
            return search_youtube_video(query[1])
    elif message.startswith("!tex"):
        query = message.split(" ", 1)
        if len(query)>1:
            return latex_to_text(query[1])
    elif message.startswith("!latex"):
        query = message.split(" ", 1)
        if len(query)>1:
            return latex_to_png(query[1])
    elif message == "!help":
        return '!corona <location> for latest coronavirus report for specified location. \n'\
                    '!news <query> for latest news related to specified query. \n'\
                    '!weather <location> for weather report at specified location. \n'\
                    '!youtube <query> to search for youtube video. \n'\
                    '!latex <query> to compile latex into png. \n'\
                    '!tex <query> to compile latex into unicode.'
    else:
        found_urls = re.findall(r'(https?://[^\s]+)', message)
        for url in found_urls:
            return get_url_info(url)

    return ""