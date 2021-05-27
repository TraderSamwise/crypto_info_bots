from multi_thread_stream_listener import MultiThreadStreamListener
from read_env import read_env
from tweepy_stream_safe import TweepyStreamSafe

read_env()


from tweet_engine_whalealert import tweet_engine_whalealert
import time
from tweet_engine_elon import tweet_engine_elon
from tweet_engine_news import tweet_engine_news


import tweepy
from apiconfig import startup

from constants import ELON_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID



class ElonStreamListener(MultiThreadStreamListener):
    def process_status(self, status):
        tweet_engine_elon(status)

class NewsStreamListener(MultiThreadStreamListener):
    def process_status(self, status):
        tweet_engine_news(status)

class WhaleAlertStreamListener(MultiThreadStreamListener):
    def process_status(self, status):
        tweet_engine_whalealert(status)

def run_stream(StreamListener, follow):
    # Connect to the Twitter API
    api = startup()
    tweet_stream = TweepyStreamSafe(auth=api.auth, listener=StreamListener())
    # '44196397' is the ID for the @elonmusk account
    print(follow)
    tweet_stream.filter(follow=follow, is_async=True)

def main():
    run_stream(ElonStreamListener, [ELON_TWITTER_ACCOUNT_ID])
    run_stream(NewsStreamListener, [DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID])
    run_stream(WhaleAlertStreamListener, [WHALEALERT_TWITTER_ACCOUNT_ID])

    while True:
        time.sleep(200)


if __name__ == "__main__":
    main()

