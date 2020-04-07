import requests
import datetime
import re
from urllib.parse import urlparse, parse_qs, urlencode
from apikeys import *
from pylatexenc.latex2text import LatexNodes2Text
from utils import json_request

def get_latest_news(query = None):

    if query:
        url = 'http://newsapi.org/v2/everything?q={}&sortBy=relevancy&apiKey={}'.format(query, newsapi_key)
    else:
        url = 'http://newsapi.org/v2/top-headlines?country=it&sortBy=publishedAt&apiKey={}'.format(newsapi_key)
        
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

    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'.format(location, openweather_key)
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
    description = item["snippet"]["description"]
    description = description[:150] if len(description) > 150 else description
    description = description.replace('\n', ' ')
    return "{} → {}".format(title, description)


def get_youtube_description(query):
    parsed_url = urlparse(query)
    url_queries = parse_qs(parsed_url.query)
    parsed_url = parsed_url._replace(netloc='invidio.us') # replace youtube into invidio.us
    invidio_url = parsed_url.geturl()

    if "v" in url_queries:
        video_id = url_queries["v"][0]
        url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(video_id, youtube_key)
        data = json_request(url)
        if not data:
            return None
        items = data["items"]
        if len(items) > 0:
            info = get_youtube_videoinfo(items[0])
            return "{} {}".format(invidio_url, info)
    

def search_youtube_video(query, music=False):

    q = {'part':'snippet', 'maxResults': 1, 'type':'video', 'q': query, 'key': youtube_key}
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
        return "{} {}".format(url, info)

    return "I haven't found anything"

def url_meta(url):
    req_url = "https://api.urlmeta.org/?url={}".format(url)
    data = json_request(req_url, headers={'Authorization': urlmeta_api_authorization})
    if not data:
        return None
    if data["result"]["status"] == "OK":
        title = data["meta"]["title"]
        if "description" in data["meta"]:
            description = data["meta"]["description"]
            description = description[:200] if len(description) > 200 else description
            description = description.replace('\n', ' ')
            return "{} → {}".format(title, description)
        return title

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
    return LatexNodes2Text().latex_to_text(formula)
