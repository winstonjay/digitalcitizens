'''
delete_tweets.py

Helps deletes all your tweets 1000 at a time.

NOTE: Requires app authentication from https://apps.twitter.com/ with read -
write privileges. You set your authentication tokens as enviroment varibles
that the app provides.

NOTE: WARNING THIS WILL DELETE 1000 TWEETS OF THE AUTHORISED ACCOUNT THAT IS
ACCESSING THE API. THIS CANNOT BE UNDONE.

.env.example:
    TWITTER_CONSUMER_KEY=your_consumer_key
    TWITTER_CONSUMER_SECRET=your_consumer_secret
    TWITTER_ACCESS_TOKEN=your_access_Token
    TWITTER_ACCESS_TOKEN_SECRET=your_access_Token_secret

You can then set these varibles for your current bash session with:
    $ for line in $(cat .env); do export $line; done
'''
from __future__ import print_function
import os
import sys
import tweepy

# python 2/3 cover.
try:
    input = raw_input
except:
    pass

# Edit theese variables with your own auth tokens if need be.
consumer_key        = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret     = os.environ["TWITTER_CONSUMER_SECRET"]
access_token        = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]


def main():
    # init api.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # get user account info via the api.
    me = api.me()
    total = min([750, me.statuses_count])
    fmt_args = (total, me.statuses_count, me.name, me.screen_name, me.id_str)

    # set verbose flag to check each tweet before deleting.
    verbose = len(sys.argv) >= 2 and sys.argv[1] == "-v"

    if input(message.format(*fmt_args)) != "y":
        print("Action Aborted")
        return

    # DANGER: WARNING THIS WILL DELETE 750 TWEETS OF THE AUTHORISED ACCOUNT THAT
    # IS ACCESSING THE API. THIS CANNOT BE UNDONE.
    for tweet in api.user_timeline(me.id, count=total):
        print("id:   {}\ntext: {}".format(tweet.id, tweet.text))
        if verbose and input("Skip tweet (y/n): ") == "y":
            continue
        api.destroy_status(tweet.id)


message = '''WARNING:

THIS TRY WILL DELETE {}/{} TWEETS OF THE AUTHORISED ACCOUNT:
    name:        {}
    screen name: {}
    id:          {}

THIS CANNOT BE UNDONE. Are you sure want to continue? (y/n): '''

if __name__ == '__main__':
    main()


