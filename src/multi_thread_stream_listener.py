from python_utils.generic_utils import get_secret_helper
import asyncio
from tweepy import asynchronous


class MultiThreadTwitterStreamListener(asynchronous.AsyncStream):
    '''
    Streams from Twitter API via Tweepy as a dedicated service
    '''

    def __init__(self, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):

        consumer_key = consumer_key or get_secret_helper("TWITTER_CONSUMER_KEY")
        consumer_secret = consumer_secret or get_secret_helper("TWITTER_CONSUMER_SECRET")
        access_token = access_token or get_secret_helper("TWITTER_ACCESS_TOKEN")
        access_token_secret = access_token_secret or get_secret_helper("TWITTER_ACCESS_SECRET")

        self.follow = []
        super().__init__(consumer_key, consumer_secret, access_token,
                         access_token_secret)


    def run_forever(self, follow):
        self.follow = follow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.filter(follow=follow))

    async def on_status(self, status):
        asyncio.create_task(self.process_status(status))

    async def process_status(self, status):
        pass
