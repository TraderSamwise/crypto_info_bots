from read_env import read_env
read_env()

from tweet_engine_whalealert import tweet_engine_whalealert
import time
from tweet_engine_elon import tweet_engine_elon
from tweet_engine_news import tweet_engine_news


import tweepy
from apiconfig import startup

from constants import ELON_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID

from threading import Thread


class ElonStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_engine_elon(status)

class NewsStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_engine_news(status)

class WhaleAlertStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_engine_whalealert(status)

def run_stream(StreamListener, follow):
    # Connect to the Twitter API
    api = startup()
    tweet_stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
    # '44196397' is the ID for the @elonmusk account
    while True:
        print("looping")
        try:
            print(follow)
            tweet_stream.filter(follow=follow, is_async=False)
        except tweepy.error.RateLimitError as e:
            print(e)
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(5)
        time.sleep(5)


threads = []
def main():
    # t1 = Thread(target=run_stream, args=(ElonStreamListener, [ELON_TWITTER_ACCOUNT_ID]))
    # t1.daemon = True
    # t1.start()
    # threads.append(t1)
    #
    # t2 = Thread(target=run_stream, args=(NewsStreamListener, [DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID]))
    # t2.daemon = True
    # t2.start()
    # threads.append(t2)
    #
    t3 = Thread(target=run_stream, args=(WhaleAlertStreamListener, [WHALEALERT_TWITTER_ACCOUNT_ID]))
    t3.daemon = True
    t3.start()
    threads.append(t3)

    # run_stream(WhaleAlertStreamListener, [WHALEALERT_TWITTER_ACCOUNT_ID])

    for x in threads:
        x.join()




if __name__ == "__main__":
    main()

