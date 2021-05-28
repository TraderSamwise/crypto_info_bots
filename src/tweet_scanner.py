
# THIS NEEDS TO BE AT THE TOP, OR IMPORTATED FILES WONT HAVE ENV VARIABLES IN DEV
from read_env import read_env
read_env()


from multi_thread_stream_listener import MultiThreadStreamListener
from tweepy_stream_safe import TweepyStreamSafe
from tweet_engine_dispatcher import tweet_engine_dispatcher


from apiconfig import startup

from constants import ELON_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID


class DispatcherStreamListener(MultiThreadStreamListener):
    def process_status(self, status):
        tweet_engine_dispatcher(status)

def run_stream(StreamListener, follow):
    # Connect to the Twitter API
    api = startup()
    tweet_stream = TweepyStreamSafe(auth=api.auth, listener=StreamListener())
    print(follow)
    tweet_stream.filter(follow=follow)

def main():
    run_stream(DispatcherStreamListener, [ELON_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, WHALEALERT_TWITTER_ACCOUNT_ID])


if __name__ == "__main__":
    main()

