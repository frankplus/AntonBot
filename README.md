# coronavirus-irc-bot
An IRC bot for latest coronavirus reports. 

Global and countries data are retrieved from Johns Hopkins CSSE data repository using `ExpDev07/coronavirus-tracker-api` \
Italian's province and regional data are retrieved from Dipartimento di Protezione Civile `pcm-dpc/COVID-19` repository.

This bot is not just for coronavirus reports but also for news, weather, youtube search and a fun quiz game.


## Installation
```
git clone https://github.com/frankplus/coronavirus-irc-bot
cd coronavirus-irc-bot
pip install .
```
See ircbot.py and utils.py to set channel name and bot name

### Run
`python3 ircbot.py`

To run the bot in the background execute this instead:\
`nohup python3 ./ircbot.py &` 

## Commands
`!corona <location>` for latest coronavirus report for specified location. \
`!news <query>` for latest news related to specified query. \
`!weather <location>` for weather report at specified location. \
`!youtube <query>` to search for youtube video.\
`!latex <query>` to compile latex into png.\
`!tex <query>` to compile latex into unicode.\
`!music <query>` to search for music video on youtube.\
`!game [easy/medium/hard] [id_category]` to start game.

## Other features
- Cleverbot
- scan messages for urls and send reply with info about its content 