import config
from lib.utils import json_request_get
from openai import OpenAI

def _fetch_weather_data(location):
    """Internal function to fetch weather data from OpenWeatherMap API"""
    # Get location coordinates
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={config.OPENWEATHER_KEY}"
    data = json_request_get(url)
    if not data:
        return None
    
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    location_name = data[0]["name"]
    
    # Get weather data
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={config.OPENWEATHER_KEY}"
    weather_data = json_request_get(url)
    if not weather_data:
        return None
    
    # Add location name to the response for context
    weather_data["location_name"] = location_name
    return weather_data

def get_weather_api(location):
    """Get raw weather data from openweathermap API without ChatGPT analysis"""
    return _fetch_weather_data(location)

def get_weather_summary(location):
    """Get weather summary with ChatGPT analysis"""
    weather_data = _fetch_weather_data(location)
    if not weather_data:
        return None
    
    location_name = weather_data["location_name"]
    chatbot_prompt = f"give a humorous but informative weather bulletin and forecast for {location_name} in one short "\
        "paragraph in Italian given the following data retrieved from openweathermap: \n"\
        f"```\n{str(weather_data)}\n```"
    
    client = OpenAI(api_key=config.CHATGPT_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": chatbot_prompt}
        ]
    )
    response_message = response.choices[0].message.content
    return response_message

WEATHER_FUNCTION_DEFINITION = {
    "type": "function",
    "name": "get_weather_api",
    "description": "Get current weather conditions and forecast for a specified location. Returns detailed weather data including temperature, humidity, wind, and forecast.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location (city, country) to get weather information for. Examples: 'Rome, Italy', 'New York, USA', 'London, UK'"
            }
        },
        "required": ["location"],
        "additionalProperties": False
    },
    "strict": True
}

def register(bot):
    bot.register_command('weather', lambda _channel, _sender, query: get_weather_summary(query) if query else None)
    bot.register_help('weather', '!weather <location> for weather report at specified location.')
    # Register function for OpenAI function calling
    bot.register_function(get_weather_api, WEATHER_FUNCTION_DEFINITION)
