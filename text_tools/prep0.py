'''


'''
# tsv structures

# tweets heads:
#   puid                    int         unique tweet id
#   created_at              timestr
#   tweet                   string
#   tags                    string      space seperated hashtags
#   possibly_sensitive      bool
#   user_puid               int         unique user identifier
#   lang                    string

# users heads:
#   puid               int         unique user identifier for collection
#   created_at         timestr
#   followers_count    int
#   friends_count      int         number of users they follow
#   statuses_count     int
#   tweet_count        int         number of tweets in collection
#   favourites_count   int
#   id                 int
from __future__ import print_function

import argparse
import csv
import json
import sys
import random
import re
import zipfile
from datetime import datetime

from nltk.stem.snowball import SnowballStemmer


def extract_tweets(f):
    "extract tweet created_at, tags and text from each tweet json object."
    global puid, dropped, real_total
    for line in f:
        real_total += 1
        if random.random() < dropout_rate:
            dropped += 1
            continue
        tweet = json.loads(line)
        puid += 1
        yield build_row(
            puid,                                   # puid
            extract_date(tweet["created_at"]),      # created_at
            extract_user(tweet["user"]),            # user_puid
            extract_text(tweet["full_text"]),       # tweet
            extract_hashtags(tweet["entities"]),    # tags
            tweet["possibly_sensitive"],            # possibly_sensitive
            tweet["lang"])                          # lang

def build_row(*args): return tcat(str(c) if c != "" else "null" for c in args)

def extract_text(text):
    '''converts the text to lowercase remove all non words,
    stopwords, non ascii characters and links. stem the remaining
    words and concatinate the result into a new string.'''
    s = rx1.sub(' ', text.lower())
    return cat(stemmer.stem(w) for w in rx0.findall(s)
                if 3 < len(w) < 20
                if w not in stop_words)

rx0 = re.compile(r"\w+")
rx1 = re.compile(r'[^\x00-\x7F]+|\n|http\S+')

cat   = " ".join
tcat = "\t".join

stop_words_path = "../resources/more_stopwords.txt"

stop_words = set(open(stop_words_path).read().split())
stemmer    = SnowballStemmer("english")

def extract_hashtags(entities):
    "gets tags tweet by tweet returning their names seperated by spaces."
    tags = [t['text'] for t in entities["hashtags"]]
    tags = cat(tags)
    return tags if is_ascii(tags) else ""

def is_ascii(s): return all(ord(c) < 128 for c in s)


def extract_date(date):
    time = datetime.strptime(date, time_read)
    return time.strftime(time_write)

time_read  = "%a %b %d %H:%M:%S +0000 %Y"
time_write = "%d/%m/%Y %H:%M:%S"


def extract_user(user):
    global user_puid, users
    # if we already seen them just return their id.
    twiter_id = user["id_str"]
    if twiter_id in users:
        users[twiter_id]["tweet_count"] += 1
        return users[twiter_id]["puid"]
    # if we havent see them then we need to increment the user_puid and create
    # an entry for them.
    user_puid += 1
    users[twiter_id] = {
        "puid":             user_puid,
        "id":               twiter_id,
        "created_at":       extract_date(user["created_at"]),
        "followers_count":  user["followers_count"],
        "friends_count":    user["friends_count"],
        "statuses_count":   user["statuses_count"],
        "favourites_count": user["favourites_count"],
        "tweet_count":      1
    }
    return user_puid


#### Writing the files

# iterate through each file in the zipped folder, then extract tweets line by
# line writing these straight away to our output file. At the same tiem we will
# keep track of users and once we have finished writing the tweets write the
# users to a sperate tsv file.

source_filename = "../data/final/data.zip"
tweets_filename = "../data/final/tweets_small.tsv"
users_filename  = "../data/final/users_small.tsv"


users = {}  # dictionary of all the users we see in the collection.

puid = 0
user_puid = 0

total_tweets = 0   # keep track of how many tweets we collect
file_i = 1

dropout_rate = 0.8 # there are 2 million tweets and we dont need all of them
dropped = 1
real_total = 1

tweets_file = open(tweets_filename, "w")

tweets_head = tcat(
    "puid created_at user_puid tweet tags possibly_sensitive lang".split(" "))

print("writing tweets file:", tweets_filename)
with zipfile.ZipFile(source_filename) as z:
    files_count = len(z.namelist()) -1
    tweets_file.write(tweets_head)
    tweets_file.write("\n")
    for filename in z.namelist()[1:]:
        print("reading file: {} {}/{}. dropped: {:.2f}".format(
            filename, file_i, files_count, dropped / real_total))
        file_i += 1
        f = z.open(filename)
        for line in extract_tweets(f):
            tweets_file.write(line)
            tweets_file.write("\n")
            total_tweets += 1
        f.close()

tweets_file.close()

user_rows = list(users.values())
print("- " * 40)
print("total tweets", total_tweets)
print("total users", len(users))
print("- " * 40)
print("writing users file:", users_filename)

with open(users_filename, "w") as users_file:
    fieldnames = list(user_rows[0].keys())
    writer = csv.DictWriter(users_file, fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(user_rows)

print("- " * 40)
print("finished")