from lib.utils import json_request_get

irc_formatting = True

def format(number, sign = False):
    if irc_formatting:
        if sign:
            return '\x02\x0304{:+}\x03\x02'.format(number)
        else:
            return '\x02\x0304{}\x03\x02'.format(number)
    else:
        if sign:
            return '{:+}'.format(number)
        else:
            return str(number)


def get_country_status(query):
    data = json_request_get('https://api.covid19api.com/summary')
    if not data:
        return None

    for country in data["Countries"]:
        if country["Country"].lower() == query or country["Slug"] == query or country["CountryCode"].lower() == query:
            confirmed = format(country["TotalConfirmed"])
            new_cases = format(country["NewConfirmed"], sign=True)
            deaths = format(country["TotalDeaths"])
            new_deaths = format(country["NewDeaths"], sign=True)

            info = 'Total Cases: {} ({}) - Total Deaths: {} ({})'.format(confirmed, new_cases, deaths, new_deaths)
            return info

def get_italy_status():
    data = json_request_get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json')
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

def get_colore_regione(query):
    data = json_request_get("https://covid19.zappi.me/coloreRegioni.php")
    for color in data:
        for regione in data[color]:
            print(regione)
            if regione.lower() == query.lower():
                return f"Zona {color}"
    return "Zona sconosciuta"

def get_italy_regione(query):
    data = json_request_get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
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
            colore = get_colore_regione(query)

            info = 'Attualmente positivi: {} ({}) - Dimessi guariti: {} - Deceduti: {} - Totale casi: {} ({}) - Tamponi: {} - {}' \
                    .format(totale_positivi, variazione_totale_positivi, dimessi_guariti, deceduti, totale_casi, nuovi_positivi, tamponi, colore)

            return info

def get_italy_province(query):
    data = json_request_get('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json')
    if not data:
        return None

    for provincia in data:
        if provincia["denominazione_provincia"].lower() == query:
            totale_casi = format(provincia["totale_casi"])
            
            info = 'Totale Casi: {}'.format(totale_casi)
            return info


def get_global_status():
    data = json_request_get('https://api.covid19api.com/summary')
    if not data:
        return None

    confirmed = format(data["Global"]["TotalConfirmed"])
    deaths = format(data["Global"]["TotalDeaths"])
    new_cases = format(data["Global"]["NewConfirmed"], sign=True)
    new_deaths = format(data["Global"]["NewDeaths"], sign=True)

    info = 'Total Cases: {} ({}) - Total Deaths: {} ({})'.format(confirmed, new_cases, deaths, new_deaths)
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

def register(bot):
    bot.register_command('corona', lambda channel, sender, query: elaborate_query(query) if query else None)
    bot.register_help('corona', '!corona <location> for latest coronavirus report for specified location.')
