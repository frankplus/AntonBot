import requests
import random
import corona
import datetime
import re
from urllib.parse import urlparse, parse_qs
from apikeys import newsapi_key, openweather_key, youtube_key


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
    url_data = urlparse(query)
    video_id = parse_qs(url_data.query)["v"][0]
    url = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(video_id, youtube_key)
    data = requests.get(url).json()
    items = data["items"]
    if len(items) > 0:
        title = items[0]["snippet"]["title"]
        description = items[0]["snippet"]["description"]
        description = description[:150] if len(description) > 150 else description
        hooktube_url = query.replace("youtube", "hooktube")
        return "{} {} - {}".format(hooktube_url, title, description)
    
    return ""


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
    elif message == "!help":
        return '!corona <location> for latest coronavirus report for specified location. '\
                    '!news <query> for latest news related to specified query. '\
                    '!weather <location> for weather report at specified location. '

    found_urls = re.findall(r'(https?://[^\s]+)', message)
    for url in found_urls:
        response = get_youtube_description(url)
        if response:
            return response

    return ""