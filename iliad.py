#!/usr/bin/env python
import re
import requests
from bs4 import BeautifulSoup
import datetime
import json

PATTERNS = {
    'nome': r'<div class=\"bold\">(.*)</div>',
    'id': r'ID utente: (\d+.\d+)',
    'numero': r'Numero: (\d+.\d+.\d+)',
    'credito': r'- Credito : <b class="red">(\d.+.(.|,)?)</b>',
    'chiamate': 'Chiamate: <span class="red">(.*)</span><br/>', 
    'sms': r'<div class="conso__text"><span class="red">(\d+) SMS</span>', 
    'mms': r'<span class="red">(\d+) MMS<br/></span>', 
    'dati': '<span class="red">(.*)</span> / (.*)<br/>',
    'data_rinnovo': r'La tua offerta iliad si rinnoverà alle (\d+:\d+) del (\d+\/\d+\/\d+)'
}

def parse_account(html):

    info = dict()
    info["nome"] = re.compile(PATTERNS['nome']).search(str(html)).group(1)
    info["id"] = re.compile(PATTERNS['id']).search(html.text).group(1)
    info["numero"] = re.compile(PATTERNS['numero']).search(html.text).group(1)
    info["credito"] = re.compile(PATTERNS['credito']).search(str(html)).group(1)
    info["data_rinnovo"] = re.compile(PATTERNS['data_rinnovo']).search(str(html)).group(2)

    consumi_italia = dict()
    consumi_estero = dict()

    chiamate = re.findall(re.compile(PATTERNS['chiamate']), str(html))
    consumi_italia['chiamate'] = chiamate[0]
    consumi_estero['chiamate'] = chiamate[1]

    sms = re.findall(re.compile(PATTERNS['sms']), str(html))
    consumi_italia['sms'] = sms[0]
    consumi_estero['sms'] = sms[1]

    mms = re.findall(re.compile(PATTERNS['mms']), str(html))
    consumi_italia['mms'] = mms[0]
    consumi_estero['mms'] = mms[1]

    dati = re.findall(re.compile(PATTERNS['dati']), str(html))
    consumi_italia['dati'] = dati[0][0]
    consumi_italia['totale_dati'] = dati[0][1]
    consumi_estero['dati'] = dati[1][0]
    consumi_estero['totale_dati'] = dati[1][1]

    data = {
        'info': info,
        'consumi_italia': consumi_italia,
        'consumi_estero': consumi_estero
    }

    return data

def get_info(user, password):

    ACCOUNT_URL = "https://www.iliad.it/account/"

    with requests.session() as s:
        # fetch the login page
        s.get(ACCOUNT_URL)
        s.get(ACCOUNT_URL, params={'logout': 'user'})

        # post to the login form
        login_info = {'login-ident': user, 'login-pwd': password}
        response = s.post(ACCOUNT_URL, data=login_info)
        html = BeautifulSoup(response.content, "html.parser")

    if "ID utente o password non corretto." in html.text:
        return None
    else:
        return parse_account(html)

def parse_dati_to_gb(dati):
    regex = re.compile(r'(\d+,?\d*)(GB|mb|MB|KB|b)')
    match = regex.match(dati)
    if match:
        value = float(match.group(1).replace(',', '.'))
        exp_table = {
            'GB': 1.0,
            'mb': 2**10,
            'MB': 2**10,
            'KB': 2**20,
            'b': 2**30,
        }
        return value / exp_table.get(match.group(2))

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%d/%m/%Y')

def totale_dati_giornalieri(login_info, print_log=False):
    all_accounts = [get_info(user_id, pwd) for user_id, pwd in login_info]

    if print_log:
        print(json.dumps(all_accounts, indent=4))

    totale_dati_giornalieri = 0

    for account in all_accounts:
        consumo = parse_dati_to_gb(account["consumi_italia"]["dati"])
        totale = parse_dati_to_gb(account["consumi_italia"]["totale_dati"])
        rimanenti = totale - consumo
        data_rinnovo = parse_date(account["info"]["data_rinnovo"])
        giorni_rimanenti = (data_rinnovo - datetime.datetime.now()).total_seconds() / (60*60*24)
        dati_rimanenti_giornalieri = rimanenti / giorni_rimanenti if giorni_rimanenti > 0 else 0
        totale_dati_giornalieri += dati_rimanenti_giornalieri

        if print_log:
            print(account["info"]["numero"])
            print("dati consumati: " + str(consumo))
            print("rimanenti: " + str(rimanenti))
            print("giorni_rimanenti: " + str(giorni_rimanenti))
            print()

    if print_log:
        print("totale_dati_giornalieri: " + str(totale_dati_giornalieri))
        
    return totale_dati_giornalieri