from utils import json_request

irc_formatting = True

def format(number, sign = False):
    if irc_formatting:
        if sign:
            return '\x02\x0304{:+}\x03\x02'.format(number)
        else:
            return '\x02\x0304{}\x03\x02'.format(number)
    else:
        return str(number)

def get_country_status(query):
    data = json_request('https://coronavirus-tracker-api.herokuapp.com/v2/locations')
    if not data:
        return None

    for location in data["locations"]:
        if (location["country"].lower() == query and location["province"] == "") or location["province"].lower() == query:
            id = location["id"]
            confirmed = format(location["latest"]["confirmed"])
            deaths = format(location["latest"]["deaths"])

            data = json_request('https://coronavirus-tracker-api.herokuapp.com/v2/locations/' + str(id))
            if not data:
                return None

            #confirmed
            timeline = data["location"]["timelines"]["confirmed"]["timeline"]
            new_cases = format(timeline.popitem()[1] - timeline.popitem()[1], sign = True)

            #deaths
            timeline = data["location"]["timelines"]["deaths"]["timeline"]
            new_deaths = format(timeline.popitem()[1] - timeline.popitem()[1], sign = True)

            info = 'Total Cases: {} ({}) - Total Deaths: {} ({})'.format(confirmed, new_cases, deaths, new_deaths)
            return info

def get_italy_status():
    data = json_request('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json')
    if not data:
        return None

    latest = data[-1]
    yesterday = data[-2]
    totale_positivi = format(latest["totale_positivi"])
    variazione_totale_positivi = format(latest["variazione_totale_positivi"], sign = True)
    nuovi_positivi = format(latest["nuovi_positivi"], sign = True)
    deceduti = format(latest["deceduti"])
    nuovi_deceduti = format(latest["deceduti"] - yesterday["deceduti"], sign = True)
    dimessi = format(latest["dimessi_guariti"])
    nuovi_dimessi = format(latest["dimessi_guariti"] - yesterday["dimessi_guariti"], sign = True)
    totale_casi = format(latest["totale_casi"])

    info = 'Totale attualmente positivi: {} ({}) - Deceduti: {} ({}) - Dimessi guariti: {} ({}) - Totale casi: {} ({})' \
            .format(totale_positivi, variazione_totale_positivi, deceduti, nuovi_deceduti, dimessi, nuovi_dimessi, totale_casi, nuovi_positivi)
    
    return info

def get_italy_regione(query):
    data = json_request('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
    if not data:
        return None

    for regione in data:
        if regione["denominazione_regione"].lower() == query:
            totale_positivi = format(regione["totale_positivi"])
            variazione_totale_positivi = format(regione["variazione_totale_positivi"], sign = True)
            nuovi_positivi = format(regione["nuovi_positivi"], sign = True)
            dimessi_guariti = format(regione["dimessi_guariti"])
            deceduti = format(regione["deceduti"])
            totale_casi = format(regione["totale_casi"])
            tamponi = format(regione["tamponi"])

            info = 'Attualmente positivi: {} ({}) - Dimessi guariti: {} - Deceduti: {} - Totale casi: {} ({}) - Tamponi: {}' \
                    .format(totale_positivi, variazione_totale_positivi, dimessi_guariti, deceduti, totale_casi, nuovi_positivi, tamponi)

            return info

def get_italy_province(query):
    data = json_request('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json')
    if not data:
        return None

    for provincia in data:
        if provincia["denominazione_provincia"].lower() == query:
            totale_casi = format(provincia["totale_casi"])
            
            info = 'Totale Casi: {}'.format(totale_casi)
            return info


def get_global_status():
    data = json_request('https://coronavirus-tracker-api.herokuapp.com/v2/latest')
    if not data:
        return None

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
