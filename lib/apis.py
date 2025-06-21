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
import json

logging.getLogger().setLevel(logging.DEBUG)

class Chatbot:
    def __init__(self):
        self.client = OpenAI(api_key=CHATGPT_KEY)
        self._load_functions()

    def _load_functions(self):
        """Load available functions from plugins"""
        self.available_functions = {}
        self.function_definitions = []
        
        # Load news function
        try:
            from plugins.news import get_latest_news, NEWS_FUNCTION_DEFINITION
            self.available_functions["get_latest_news"] = get_latest_news
            self.function_definitions.append(NEWS_FUNCTION_DEFINITION)
        except ImportError as e:
            logging.warning(f"Could not load news plugin: {e}")

    def elaborate_query(self, conversation, image_input_url=None):
        try:
            messages = [
                {
                    "role": "developer",
                    "content": CHATBOT_PROMPT
                },
                {
                    "role": "user",
                    "content": '\n'.join(conversation)
                }
            ]

            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=messages,
                tools=self.function_definitions,
                tool_choice="auto"
            )

            logging.debug(f"ChatGPT response: {response}")

            response_message = response.choices[0].message
            
            # Check if the model wants to call a function
            if response_message.tool_calls:
                # Execute function calls
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name in self.available_functions:
                        function_response = self.available_functions[function_name](**function_args)
                        
                        # Add function response to conversation
                        messages.append(response_message)
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": str(function_response)
                        })
                
                # Get final response with function results
                final_response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                response_message = final_response.choices[0].message.content
            else:
                response_message = response_message.content

            # remove bot name
            if response_message:
                pos = response_message.find(BOTNAME)
                if pos == 0:
                    split = response_message.split(' ', 1)
                    if len(split) > 1:
                        response_message = split[1]
            
            return response_message
        except Exception as e:
            logging.error(f"Failed to send request to chatgpt: {e}")
            return None

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
