# coronavirus-irc-bot
An IRC/telegram bot for latest coronavirus reports and more. 

Global and countries data are retrieved from Johns Hopkins CSSE data repository using `ExpDev07/coronavirus-tracker-api` \
Italian's province and regional data are retrieved from Dipartimento di Protezione Civile `pcm-dpc/COVID-19` repository.

This bot is not just for coronavirus reports but also for news, youtube search, wolfram queries, a fun quiz game and more listed below.


## Installation
```
git clone https://github.com/frankplus/coronavirus-irc-bot
cd coronavirus-irc-bot
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
See config.py to set irc configurations and api keys.

### Run
If you want to run only the IRC bot:
`python3 ircbot.py`

If you want to run only the telegram bot:
`python3 telegrambot.py`


If you want to run both the IRC and the telegrambot:
`python3 run_irc_telegram.py`

### Test
If you just want to test the bot run `python3 test.py`

## Commands
`!corona <location>` for latest coronavirus report for specified location. \
`!news <query>` for latest news related to specified query. \
`!weather <location>` for weather report at specified location. \
`!youtube <query>` to search for youtube video.\
`!image <query>` to search for an image.\
`!latex <query>` to compile latex into png.\
`!tex <query>` to compile latex into unicode.\
`!music <query>` to search for music video on youtube.\
`!game [easy/medium/hard] [id_category]` to start game.\
`!wolfram <query>` to calculate or ask wolfram any question.\
`!plot <query>` to plot any mathematical function.\
`!chess <query>` to play a chess game..

## Other features
- Cleverbot
- scan messages for urls and send reply with info about its content 
- Pulls RSS feeds from miniflux for latest updates