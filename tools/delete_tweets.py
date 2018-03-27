'''
delete_tweets.py

Helps deletes all your tweets 1000 at a time.

NOTE: WARNING THIS WILL DELETE APPROXIMATELY 750 TWEETS OF THE AUTHORISED
ACCOUNT THAT IS ACCESSING THE API. THIS CANNOT BE UNDONE.

NOTE: Requires app authentication from https://apps.twitter.com/ with read -
write privileges. You set your authentication tokens as enviroment varibles
that the app provides.

Enviroment varibles need to be set. this can be done by creating a .env file
as follows:

  TWITTER_CONSUMER_KEY=your_consumer_key
  TWITTER_CONSUMER_SECRET=your_consumer_secret
  TWITTER_ACCESS_TOKEN=your_access_Token
  TWITTER_ACCESS_TOKEN_SECRET=your_access_Token_secret

You can then set the env varibles with:

  $ for line in $(cat .env); do export $line; done

Alternatively just set your env varibles directly. Search 'EDIT_HERE' to see
where to do this.
'''
from __future__ import print_function

import os
import sys
import argparse

import tweepy

# python 2/3 cover.
try:
  input = raw_input
except:
  pass

### EDIT_HERE
# You can just replace all of this by just setting your env varibles directly.
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
  args = parse_args()
  me = api.me()
  total = 750
  message_args = (total, me.statuses_count, me.name, me.screen_name, me.id_str)

  # Check if user actually wants to do this.
  if input(message.format(*message_args)) != "y":
    print("Action Aborted")
    return

  kwargs = {'count': total, 'max_id': args.max_id, 'since_id': args.max_id}
  # DANGER: WARNING THIS WILL DELETE 750 TWEETS OF THE AUTHORISED ACCOUNT THAT
  # IS ACCESSING THE API. THIS CANNOT BE UNDONE.
  for tweet in api.user_timeline(me.id, **kwargs):
    if args.verbose:
      print("id:   {}\ntext: {}".format(tweet.id, tweet.text))
      if input("Skip tweet (y/n): ") == "y":
        continue
    api.destroy_status(tweet.id)
    print("Deleted tweet: {}. From: {}".format(tweet.id, tweet.created_at))


def parse_args():
  "Parse args and return formatted args."
  help_link = "https://goo.gl/89ikje"
  parser = argparse.ArgumentParser(description="Delete unwanted tweets")
  parser.add_argument('-v', '--verbose',
    type=bool, help='check each Tweet before deleting', default=True)
  parser.add_argument('-m', '--max_id',
    type=int, help='Newest tweet by incremental id. Info: %s' % help_link, default=None)
  parser.add_argument('-s', '--since_id',
    type=int, help='Oldest tweet by incremental id. Info: %s' % help_link, default=None)
  return parser.parse_args()

message = '''WARNING:

THIS TRY WILL DELETE {}/{} TWEETS OF THE AUTHORISED ACCOUNT:
  name:        {}
  screen name: {}
  id:          {}

THIS CANNOT BE UNDONE. Are you sure want to continue? (y/n): '''

if __name__ == '__main__':
  main()


