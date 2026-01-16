from config import *
from lib.utils import http_request_get
from bs4 import BeautifulSoup
import logging
from openai import OpenAI
import json

logging.getLogger().setLevel(logging.DEBUG)

class Chatbot:
    def __init__(self, plugin_bot=None):
        self.client = OpenAI(
            api_key=GROK_API_KEY,
            base_url="https://api.x.ai/v1",
        )
        self.plugin_bot = plugin_bot
        if plugin_bot:
            # Use plugin bot's function definitions
            self.available_functions = plugin_bot.get_available_functions()
            self.function_definitions = plugin_bot.get_function_definitions()

    def elaborate_query(self, conversation, image_input_url=None):
        try:
            # Convert conversation list to message format
            # conversation is a list of strings "Sender: message"
            # We need to parse it slightly better or just dump it in user prompt?
            # Existing code was doing: '\n'.join(conversation) as user content.
            # We will keep that structure.
            
            input_messages = [
                {
                    "role": "system", 
                    "content": CHATBOT_PROMPT
                },
                {
                    "role": "user",
                    "content": '\n'.join(conversation)
                }
            ]

            kwargs = {
                "model": "grok-4-1-fast-non-reasoning",
                "messages": input_messages,
            }
            if self.function_definitions:
                kwargs["tools"] = self.function_definitions
                kwargs["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**kwargs)

            logging.debug(f"Grok response: {response}")
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Append the assistant's response (with tool calls) to history
                input_messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name in self.available_functions:
                        function_response = self.available_functions[function_name](**function_args)
                        
                        input_messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": str(function_response),
                        })
                
                # Get final response
                final_response = self.client.chat.completions.create(
                    model="grok-4-1-fast-non-reasoning",
                    messages=input_messages
                )
                logging.debug(f"Final response after function calls: {final_response}")
                response_text = final_response.choices[0].message.content
            else:
                response_text = response_message.content

            # remove bot name if present
            if response_text:
                pos = response_text.find(BOTNAME)
                if pos == 0:
                    split = response_text.split(' ', 1)
                    if len(split) > 1:
                        response_text = split[1]
            
            return response_text
        except Exception as e:
            logging.error(f"Failed to send request to grok: {e}")
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
