#!/usr/bin/python3

import sys
import requests

def format(text):
    return '\x02\x034{}\x03\x02'.format(text)

def get_country_status(query):
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')
    data = r.json()

    for location in data["locations"]:
        if location["country"].lower() == query and location["province"] == "":
            id = location["id"]
            confirmed = format(location["latest"]["confirmed"])
            deaths = format(location["latest"]["deaths"])

            r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations/' + str(id))
            data = r.json()

            #confirmed
            timeline = data["location"]["timelines"]["confirmed"]["timeline"]
            new_cases = format(timeline.popitem()[1] - timeline.popitem()[1])

            #deaths
            timeline = data["location"]["timelines"]["deaths"]["timeline"]
            new_deaths = format(timeline.popitem()[1] - timeline.popitem()[1])

            info = 'Total Cases: {} (+{}) - Total Deaths: {} (+{})'.format(confirmed, new_cases, deaths, new_deaths)
            return info

def get_italy_status():
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json')
    data = r.json()
    latest = data[-1]
    yesterday = data[-2]
    totale_attualmente_positivi = format(latest["totale_attualmente_positivi"])
    nuovi_attualmente_positivi = format(latest["nuovi_attualmente_positivi"])
    deceduti = format(latest["deceduti"])
    nuovi_deceduti = format(latest["deceduti"] - yesterday["deceduti"])
    dimessi = format(latest["dimessi_guariti"])
    nuovi_dimessi = format(latest["dimessi_guariti"] - yesterday["dimessi_guariti"])
    totale_casi = format(latest["totale_casi"])

    info = 'Totale attualmente positivi: {} (+{}) - Deceduti: {} (+{}) - Dimessi guariti: {} (+{}) - Totale casi: {}' \
            .format(totale_attualmente_positivi, nuovi_attualmente_positivi, deceduti, nuovi_deceduti, dimessi, nuovi_dimessi, totale_casi)
    
    return info

def get_italy_regione(query):
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
    data = r.json()
    for regione in data:
        if regione["denominazione_regione"].lower() == query:
            totale_attualmente_positivi = format(regione["totale_attualmente_positivi"])
            nuovi_attualmente_positivi = format(regione["nuovi_attualmente_positivi"])
            dimessi_guariti = format(regione["dimessi_guariti"])
            deceduti = format(regione["deceduti"])
            totale_casi = format(regione["totale_casi"])
            tamponi = format(regione["tamponi"])

            info = 'Attualmente positivi: {} (+{}) - Dimessi guariti: {} - Deceduti: {} - Totale casi: {} - Tamponi: {}' \
                    .format(totale_attualmente_positivi, nuovi_attualmente_positivi, dimessi_guariti, deceduti, totale_casi, tamponi)

            return info

def get_italy_province(query):
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json')
    data = r.json()
    for provincia in data:
        if provincia["denominazione_provincia"].lower() == query:
            totale_casi = format(provincia["totale_casi"])
            
            info = 'Totale Casi: {}'.format(totale_casi)
            return info


def get_global_status():
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/latest')
    data = r.json()

    confirmed = format(data["latest"]["confirmed"])
    deaths = format(data["latest"]["deaths"])

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
        

print(elaborate_query(sys.argv[1]))

