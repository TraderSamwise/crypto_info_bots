# THIS NEEDS TO BE AT THE TOP, OR IMPORTATED FILES WONT HAVE ENV VARIABLES IN DEV
import os

from python_utils.read_env import read_env
is_prod = os.getenv("PRODUCTION")
if not is_prod:
    read_env()



from multi_thread_stream_listener import MultiThreadTwitterStreamListener
from tweet_engine_dispatcher import tweet_engine_dispatcher

from constants import DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID, LIVESQUAWK_TWITTER_ACCOUNT_ID, DB_TWITTER_ACCOUNT_ID, \
    COINBASE_PRO_TWITTER_ACCOUNT_ID, CZ_TWITTER_ACCOUNT_ID

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")

class DispatcherStream(MultiThreadTwitterStreamListener):
    def __init__(self):
        super().__init__(consumer_key, consumer_secret, access_token,
                         access_token_secret)

    def process_status(self, status):
        tweet_engine_dispatcher(status)


def main():
    stream = DispatcherStream()
    follow = [
        CZ_TWITTER_ACCOUNT_ID,
        DELTAONE_TWITTER_ACCOUNT_ID,
        FIRSTSQUAWK_TWITTER_ACCOUNT_ID,
        LIVESQUAWK_TWITTER_ACCOUNT_ID,
        DB_TWITTER_ACCOUNT_ID,
        COINBASE_PRO_TWITTER_ACCOUNT_ID,
        WHALEALERT_TWITTER_ACCOUNT_ID
    ]
    print(follow)
    stream.run_forever(follow)
    # sleep(10000)




if __name__ == "__main__":
    main()
#
