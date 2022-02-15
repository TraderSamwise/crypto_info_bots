import tweepy
from queue import Queue
from threading import Thread


class MultiThreadStreamListener(tweepy.Stream):
    def run_forever(self, follow):
        self.q = Queue()
        num_worker_threads = 4
        for i in range(num_worker_threads):
            t = Thread(target=self.do_stuff)
            t.daemon = True
            t.start()
        self.filter(follow=follow)

    def on_status(self, status):
        self.q.put(status)


    def process_status(self, status):
        pass

    def do_stuff(self):
        while True:
            self.process_status(self.q.get())
            self.q.task_done()