import JustIRC
import random
import requests

def get_country_status(country):
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')
    data = r.json()

    for location in data["locations"]:
        if location["country"].lower() == country  and location["province"] == "":
            id = location["id"]
            confirmed = location["latest"]["confirmed"]
            deaths = location["latest"]["deaths"]

            r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations/' + str(id))
            data = r.json()
            
            #confirmed
            timeline = data["location"]["timelines"]["confirmed"]["timeline"]
            new_cases = timeline.popitem()[1] - timeline.popitem()[1]

            #deaths
            timeline = data["location"]["timelines"]["deaths"]["timeline"]
            new_deaths = timeline.popitem()[1] - timeline.popitem()[1]

            info = "Total Cases: " + str(confirmed) + " - Total Deaths: " + str(deaths) + " - New Cases: " + str(new_cases) + " - New Deaths: " + str(new_deaths)
            return info

def get_global_status():
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/latest')
    data = r.json()

    confirmed = data["latest"]["confirmed"]
    deaths = data["latest"]["deaths"]

    info = "Total Cases: " + str(confirmed) + " - Total Deaths: " + str(deaths)
    return info


bot = JustIRC.IRCConnection()

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!"
]

def on_connect(bot):
    bot.set_nick("CovidBot")
    bot.send_user_packet("CovidBot")

def on_welcome(bot):
    bot.join_channel("#bugbyte-ita")

def on_message(bot, channel, sender, message):
    if "hi" in message.lower() or "hello" in message.lower():
        greeting_message = random.choice(greetings).format(sender)
        bot.send_message(channel, greeting_message)
    elif "!corona" in message:
        country = message.split(" ", 1)[1].lower()
        if country == "global":
            bot.send_message(channel, get_global_status())
        elif country == "boris johnson":
            bot.send_message(channel, "Happy Hunger Games!")
        else:
            info = get_country_status(country)
            bot.send_message(channel, info)


bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)

bot.connect("irc.freenode.net")
bot.run_loop()

