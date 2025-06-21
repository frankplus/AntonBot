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
        
        # Load weather function
        try:
            from plugins.weather import get_weather_api, WEATHER_FUNCTION_DEFINITION
            self.available_functions["get_weather_api"] = get_weather_api
            self.function_definitions.append(WEATHER_FUNCTION_DEFINITION)
        except ImportError as e:
            logging.warning(f"Could not load weather plugin: {e}")

    def elaborate_query(self, conversation, image_input_url=None):
        try:
            input_messages = [
                {
                    "role": "developer",
                    "content": CHATBOT_PROMPT
                },
                {
                    "role": "user",
                    "content": '\n'.join(conversation)
                }
            ]

            response = self.client.responses.create(
                model="gpt-4.1",
                input=input_messages,
                tools=self.function_definitions if self.function_definitions else None,
                tool_choice="auto",
                parallel_tool_calls=False
            )

            logging.debug(f"ChatGPT response: {response}")

            # Check if the model wants to call functions
            has_function_calls = (response.output and 
                                any(getattr(item, 'type', None) == 'function_call' 
                                    for item in response.output))
            
            if has_function_calls:
                # Execute function calls
                for tool_call in response.output:
                    if getattr(tool_call, 'type', None) == 'function_call':
                        function_name = tool_call.name
                        function_args = json.loads(tool_call.arguments)
                        
                        if function_name in self.available_functions:
                            function_response = self.available_functions[function_name](**function_args)
                            
                            # Add function call and response to input messages
                            input_messages.append(tool_call)
                            input_messages.append({
                                "type": "function_call_output",
                                "call_id": tool_call.call_id,
                                "output": str(function_response)
                            })
                
                # Get final response with function results
                final_response = self.client.responses.create(
                    model="gpt-4.1",
                    input=input_messages
                )
                response_message = final_response.output_text
            else:
                response_message = response.output_text

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
