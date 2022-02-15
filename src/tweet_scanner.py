# THIS NEEDS TO BE AT THE TOP, OR IMPORTATED FILES WONT HAVE ENV VARIABLES IN DEV
import os
from read_env import read_env
read_env()


from multi_thread_stream_listener import MultiThreadStreamListener
from tweet_engine_dispatcher import tweet_engine_dispatcher

from constants import ELON_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID, LIVESQUAWK_TWITTER_ACCOUNT_ID, DB_TWITTER_ACCOUNT_ID, COINBASE_PRO_TWITTER_ACCOUNT_ID

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")

class DispatcherStream(MultiThreadStreamListener):
    def __init__(self):
        super().__init__(consumer_key, consumer_secret, access_token,
                         access_token_secret)

    def process_status(self, status):
        tweet_engine_dispatcher(status)


def main():
    stream = DispatcherStream()
    follow = [
        ELON_TWITTER_ACCOUNT_ID,
        DELTAONE_TWITTER_ACCOUNT_ID,
        FIRSTSQUAWK_TWITTER_ACCOUNT_ID,
        LIVESQUAWK_TWITTER_ACCOUNT_ID,
        DB_TWITTER_ACCOUNT_ID,
        COINBASE_PRO_TWITTER_ACCOUNT_ID,
        WHALEALERT_TWITTER_ACCOUNT_ID
    ]
    stream.run_forever(follow)
    print(follow)


if __name__ == "__main__":
    main()

