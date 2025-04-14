import twitter
import logging
from config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET

def tweet(message):
    api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                    consumer_secret=TWITTER_CONSUMER_SECRET,
                    access_token_key=TWITTER_ACCESS_TOKEN_KEY,
                    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                    input_encoding='utf-8')
    try:
        status = api.PostUpdate(message)
        logging.info(status)
        link = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
        return f"Message tweeted! {link}"
    except:
        logging.exception("Could not send tweet message")
        return "Error sending tweet"

def register(bot):
    bot.register_command('tweet', lambda channel, sender, query: tweet(query))
    bot.register_help('tweet', '!tweet <message> to tweet a message')
