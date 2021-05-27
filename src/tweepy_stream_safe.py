import time
import tweepy


class TweepyStreamSafe(tweepy.Stream):
    def _run(self):
        while True:
            try:
                super()._run()
            except Exception as e:
                print(e)
            time.sleep(10)