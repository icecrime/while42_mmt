from __future__ import print_function
import sys
import threading
import time

import config
import tweepy


class Stream(object):

    class _StatsdListener(tweepy.StreamListener):

        def __init__(self, queue):
            self.queue = queue

        def on_status(self, status):
            self.queue.put(('counter', 'twitter.hashtag.while42', 1))

        def on_error(self, status_code):
            print("Twitter: on_error({})".format(status_code))

        def on_timeout(self):
            print("Twitter: on_timeout()")


    def __init__(self, run, queue, hashtags):
        conf = config.twitter
        auth = tweepy.OAuthHandler(conf['consumer_key'], conf['consumer_secret'])
        auth.set_access_token(conf['access_token_key'], conf['access_token_secret'])

        self.api = tweepy.API(auth)

        listen = Stream._StatsdListener(queue)
        listen.api = self.api

        try:
            self.twt_stream = tweepy.Stream(auth, listen)
            self.twt_stream.filter(async=True, track=hashtags)
        except tweepy.TweepError as e:
            sys.stderr.write("Failed to initialize Twitter ({})\n".format(e))
        else:
            self.run = run
            self.queue = queue
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def close(self):
        if self.thread.is_alive():  
            self.thread.join()
        self.twt_stream.disconnect()

    def _run(self):
        while self.run.is_set():
            try:
                followers = self._followers_count()
            except tweepy.TweepError as e:
                sys.stderr.write("Error fetching Twitter followers ({})\n".format(e))
            else:
                self.queue.put(('gauge', 'twitter.followers', followers))
            time.sleep(5)

    def _followers_count(self):
        return self.api.me().followers_count
