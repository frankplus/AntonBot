import requests
import datetime
from urllib.parse import urlparse, parse_qs, urlencode
from config import *
from lib.utils import json_request_get, http_request_get, http_request_post
import pypandoc
from bs4 import BeautifulSoup
import urllib
import logging
import twitter
from openai import OpenAI

logging.getLogger().setLevel(logging.DEBUG)

class Chatbot:
    def __init__(self):
        self.client = OpenAI(api_key=CHATGPT_KEY)

    def elaborate_query(self, conversation, image_input_url=None):
        try:
            response = self.client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "developer",
                        "content": CHATBOT_PROMPT
                    },
                    {
                        "role": "user",
                        "content": '\n'.join(conversation)
                    }
                ]
            )
            response_message = response.output_text
            # remove bot name
            pos = response_message.find(BOTNAME)
            if pos == 0:
                split = response_message.split(' ', 1)
                if len(split) > 1:
                    response_message = split[1]
            return response_message
        except Exception as e:
            logging.error(f"Failed to send request to chatgpt: {e}")

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
    # This function is kept here as a utility for URL info, but plugin-specific logic should be in plugins.
    from plugins.youtube import get_youtube_description
    response = get_youtube_description(url)
    if response:
        return response
    response = url_meta(url)
    if response:
        return response
