#!/usr/bin/python

import sys
import requests

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

            info = "Total Cases: " + str(confirmed) + " (+" + str(new_cases) + ")" \
                    " - Total Deaths: " + str(deaths) + " (+" + str(new_deaths) + ")" 
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
            
            info = "Attualmente positivi: " + str(totale_attualmente_positivi) + " (+" + str(nuovi_attualmente_positivi) + ")" \
                    + " - Dimessi guariti: " + str(dimessi_guariti) \
                    + " - Deceduti: " + str(deceduti) \
                    + " - Totale casi: " + str(totale_casi) \
                    + " - Tamponi: " + str(tamponi)

            return info

def get_italy_province(query):
    r = requests.get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json')
    data = r.json()
    for provincia in data:
        if provincia["denominazione_provincia"].lower() == query:
            totale_casi = provincia["totale_casi"]
            
            info = "Totale Casi: " + str(totale_casi)
            return info


def get_global_status():
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/latest')
    data = r.json()

    confirmed = data["latest"]["confirmed"]
    deaths = data["latest"]["deaths"]

    info = "Total Cases: " + str(confirmed) + " - Total Deaths: " + str(deaths)
    return info

def elaborate_query(query):
    if query == "global":
        return get_global_status()

    info = get_country_status(query)
    if info:
        return info

    info = get_italy_regione(query)
    if info:
        return info
    
    info = get_italy_province(query)
    if info:
        return info
    
    return ""
        

print(elaborate_query(sys.argv[1]))

