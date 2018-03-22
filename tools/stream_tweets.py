from __future__ import print_function
import sys
import os
import tweepy

consumer_key        = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret     = os.environ["TWITTER_CONSUMER_SECRET"]
access_token        = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = tweepy.Stream(auth=api.auth, listener=BasicStreamListener())

    terms = sys.argv[1:]
    if not terms:
        print("Usage:\n\t$ python stream_tweets.py <args>"
              "\n\nNo args. At least one tracking term needed.")
        return
    stream.filter(track=terms, async=True)

class BasicStreamListener(tweepy.StreamListener):
    "Basic stream connection service"
    def on_status(self, status):
        if status.retweeted or "RT" in status.text:
            return
        out = "\t".join([
            status.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            status.text.replace("\n", "")
        ])
        print(out)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

if __name__ == '__main__':
    main()