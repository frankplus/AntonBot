import __import__('config') as config
from lib.utils import json_request_get

def get_weather(location):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={config.OPENWEATHER_KEY}"
    data = json_request_get(url)
    if not data:
        return None
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    location_name = data[0]["name"]
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={config.OPENWEATHER_KEY}"
    data = json_request_get(url)
    if not data:
        return None
    chatbot_prompt = f"give a humorous but informative weather bulletin and forecast for {location_name} in one short "\
        "paragraph in Italian given the following data retrieved from openweathermap: \n"\
        f"```\n{str(data)}\n```"
    from openai import OpenAI
    client = OpenAI(api_key=config.CHATGPT_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": chatbot_prompt}
        ]
    )
    response_message = response.choices[0].message.content
    return response_message

def register(bot):
    bot.register_command('weather', lambda channel, sender, query: get_weather(query) if query else None)
    bot.register_help('weather', '!weather <location> for weather report at specified location.')
