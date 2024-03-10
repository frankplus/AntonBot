import requests
import datetime
from urllib.parse import urlparse, parse_qs, urlencode
from config import *
from lib.utils import json_request_get, http_request_get, http_request_post
import pypandoc
from bs4 import BeautifulSoup
import miniflux
import urllib
import emoji
import logging
import twitter
from openai import OpenAI

logging.getLogger().setLevel(logging.DEBUG)

class Chatbot:
    def __init__(self):
        self.client = OpenAI(api_key=CHATGPT_KEY)

    def elaborate_query(self, conversation, image_input_url=None):
        prompt = f"You are {BOTNAME}, a friendly Italian friend, " \
                    "participating in a group chat with your friends. " \
                    "Based on the previous conversation, generate a " \
                    f"very short reply that {BOTNAME} would likely give " \
                    "in response to the latest message in the group chat. " \
                    "Your responses should match the tone and style of the group. \n" \
                    "{BOTNAME} è un appassionato di tecnologia con una forte inclinazione per la personalizzazione e "\
                    "sperimentazione di sistemi operativi e ambienti di sviluppo. Dotato di buone conoscenze "\
                    "tecniche, mostra interesse per dispositivi mobili avanzati, software di streaming e desktop "\
                    "sharing. Ha uno stile conversazionale informale, amichevole, e apprezza l'umorismo nelle "\
                    "interazioni, usando slang e termini colloquiali. I suoi interessi includono programmazione, "\
                    "gaming, Formula 1, viaggi, e musica, riflettendo una personalità poliedrica e socievole. {BOTNAME} "\
                    "è collaborativo, supportivo, e mantiene un approccio scherzoso, rendendolo una presenza vivace nel gruppo di chat.\n"\
                    "---\n"
        
        prompt += '\n'.join(conversation)

        try:
            if not image_input_url:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}]
                )
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_input_url,
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )
            
            response_message = response.choices[0].message.content

            # remove bot name
            pos = response_message.find(BOTNAME)
            if pos == 0:
                split = response_message.split(' ', 1)
                if len(split) > 1:
                    response_message = split[1]

            return response_message

        except Exception as e:
            logging.error(f"Failed to send request to chatgpt: {e}")

    def generate_image(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url


class Miniflux:
    def __init__(self):
        self.client = miniflux.Client(MINIFLUX_URL, MINIFLUX_USER, MINIFLUX_PSW)

    def get_new_entries(self, limit = 1):
        try:
            entries = self.client.get_entries(status="unread", limit=limit)["entries"]
        except miniflux.ClientError as err:
            logging.error("miniflux client error: {}".format(err.get_error_reason()))
            return None
        except:
            logging.exception("Unexpected error getting RSS entries")
            return None

        response = ""
        for entry in entries:
            try:
                publish_date = datetime.datetime.strptime(entry["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                publish_date = datetime.datetime.strptime(entry["published_at"], "%Y-%m-%dT%H:%M:%SZ")
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
        
    data = json_request_get(url)
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
    #get geo location
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHER_KEY}"
    data = json_request_get(url)
    if not data:
        return None
    
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    location_name = data[0]["name"]

    # get weather data
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={OPENWEATHER_KEY}"
    data = json_request_get(url)
    if not data:
        return None
    
    # ask chatgpt for bulletin
    chatbot_prompt = f"give a  weather humorous bulletin for {location_name} in a short "\
        "paragraph given the following data retrieved from openweathermap: \n"\
        f"```\n{str(data)}\n```"

    client = OpenAI(api_key=CHATGPT_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": chatbot_prompt}
        ]
    )

    response_message = response.choices[0].message.content
    return response_message

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
    url = "https://www.googleapis.com/youtube/v3/search?"+urlencode(q)
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

def url_meta(url):
    resp = http_request_get(url)
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
    resp = http_request_get(url)
    if resp:
        return resp.text.replace('\n', '. ')

def plot_function(query):
    q = {'q': query}
    q = urllib.parse.urlencode(q)
    return f'https://frankplus.github.io/plasm?{q}'

def emojize(query):
    return emoji.emojize(query, use_aliases=True)


def tweet(message):
    api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                    consumer_secret=TWITTER_CONSUMER_SECRET,
                    access_token_key=TWITTER_ACCESS_TOKEN_KEY,
                    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                    input_encoding='utf-8')
    try:
        status = api.PostUpdate(message)
        logging.info(status)
        link = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
        return f"Message tweeted! {link}"
    except:
        logging.exception("Could not send tweet message")
        return "Error sending tweet"

def fortune():
    return json_request_get("http://yerkee.com/api/fortune")['fortune']
