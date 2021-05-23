import time

import tweepy
from apiconfig import startup
from constants import TWITTER_ACCOUNT_ID
from tweets import tweet_engine
import os
import re
from urllib3.exceptions import ProtocolError


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_engine(status)


def main():
    # Connect to the Twitter API
    api = startup()
    elon_tweet_listener = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    # '44196397' is the ID for the @elonmusk account
    while True:
        print("looping")
        try:
            elon_tweet_listener.filter(follow=[TWITTER_ACCOUNT_ID])
        except tweepy.error.RateLimitError as e:
            print(e)
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(5)


def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''

    if content == '':
        try:
            with open('../.env') as f:
                content = f.read()
        except IOError:
            content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)

if __name__ == "__main__":
    read_env()
    main()

