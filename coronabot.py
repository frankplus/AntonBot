#!/usr/bin/python3
import JustIRC
import random
import requests

channel = "#bugbyte-ita"
botname = "CovidBot"
irc_server_address = "irc.freenode.net"
bot_call_command = "!corona"

def get_country_status(query):
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')
    data = r.json()

    for location in data["locations"]:
        if location["country"].lower() == query and location["province"] == "":
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

            info = 'Total Cases: \x02{}\x02 (+\x02{}\x02) - Total Deaths: \x02{}\x02 (+\x02{}\x02)' \
                    .format(confirmed, new_cases, deaths, new_deaths)
            return info

def get_italy_status():
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json')
    data = r.json()
    latest = data[-1]
    yesterday = data[-2]
    totale_attualmente_positivi = str(latest["totale_attualmente_positivi"])
    nuovi_attualmente_positivi = str(latest["nuovi_attualmente_positivi"])
    deceduti = str(latest["deceduti"])
    nuovi_deceduti = str(latest["deceduti"] - yesterday["deceduti"])
    dimessi = str(latest["dimessi_guariti"])
    nuovi_dimessi = str(latest["dimessi_guariti"] - yesterday["dimessi_guariti"])
    totale_casi = str(latest["totale_casi"])

    info = 'Totale attualmente positivi: {} (+{}) - Deceduti: {} (+{}) - Dimessi guariti: {} (+{}) - Totale casi: {}' \
            .format(totale_attualmente_positivi, nuovi_attualmente_positivi, deceduti, nuovi_deceduti, dimessi, nuovi_dimessi, totale_casi)
    
    return info

def get_italy_regione(query):
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
    data = r.json()
    for regione in data:
        if regione["denominazione_regione"].lower() == query:
            totale_attualmente_positivi = regione["totale_attualmente_positivi"]
            nuovi_attualmente_positivi = regione["nuovi_attualmente_positivi"]
            dimessi_guariti = regione["dimessi_guariti"]
            deceduti = regione["deceduti"]
            totale_casi = regione["totale_casi"]
            tamponi = regione["tamponi"]

            info = 'Attualmente positivi: {} (+{}) - Dimessi guariti: {} - Deceduti: {} - Totale casi: {} - Tamponi: {}' \
                    .format(totale_attualmente_positivi, nuovi_attualmente_positivi, dimessi_guariti, deceduti, totale_casi, tamponi)

            return info

def get_italy_province(query):
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json')
    data = r.json()
    for provincia in data:
        if provincia["denominazione_provincia"].lower() == query:
            totale_casi = provincia["totale_casi"]
            
            info = 'Totale Casi: {}'.format(totale_casi)
            return info


def get_global_status():
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/latest')
    data = r.json()

    confirmed = data["latest"]["confirmed"]
    deaths = data["latest"]["deaths"]

    info = 'Total Cases: {} - Total Deaths: {}'.format(confirmed, deaths)
    return info

def elaborate_query(query):
    if query == "global":
        return get_global_status()
    
    if query == "italy" or query == "italia":
        return get_italy_status()

    info = get_country_status(query)
    if info:
        return info

    info = get_italy_regione(query)
    if info:
        return info
    
    info = get_italy_province(query)
    if info:
        return info
    
    return "I don't know bro"


bot = JustIRC.IRCConnection()

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!",
    "sup?"
]

def on_connect(bot):
    bot.set_nick(botname)
    bot.send_user_packet(botname)

def on_welcome(bot):
    bot.join_channel(channel)

def on_message(bot, channel, sender, message):
    message = message.strip().lower()
    if message in ["hi", "hello", "yo", "hey"] or botname in message :
        greeting_message = random.choice(greetings).format(sender)
        bot.send_message(channel, greeting_message)
    elif message.startswith(bot_call_command):
        query = message.split(" ", 1)[1]
        if query == "boris johnson":
            bot.send_message(channel, "Happy Hunger Games!")
        else:
            info = elaborate_query(query)
            bot.send_message(channel, info)


bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)

bot.connect(irc_server_address)
bot.run_loop()

