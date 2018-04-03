from __future__ import print_function
import sys
import os
import tweepy

consumer_key        = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret     = os.environ["TWITTER_CONSUMER_SECRET"]
access_token        = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

def main():
    terms = sys.argv[1:]
    if len(terms) == 0:
        print("Usage: $ python stream_tweets.py <args>",
              "\nNo args. At least one tracking term needed.")
        return
    # Set api auth.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # Handle connection to the stream.
    stream = tweepy.Stream(auth=api.auth, listener=BasicStreamListener())
    stream.filter(track=terms, async=True)


class BasicStreamListener(tweepy.StreamListener):
    "Basic Listener for tweepy streaming API connection service"

    def on_status(self, status):
        # We will ignore retweets and just print the data and tweet text.
        if not (status.retweeted or "RT" in status.text):
            str_time = status.created_at.strftime("%Y-%m-%d %H:%M:%S")
            text = status.text.replace("\n", "")
            print(tabulate([str_time, text]))

    def on_error(self, status_code):
        # 420 = chill out on your stream. Returning False in on_data
        # disconnects the stream.
        if status_code == 420:
            return False

tabulate = "\t".join

if __name__ == '__main__':
    main()