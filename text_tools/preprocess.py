# -*- coding: utf-8 -*-
'''
preprocess.py

eg usage:
    python3.6 preprocess.py tweets_22-2-18 -o tweets -f extended
'''
from __future__ import print_function

import argparse
import csv
import json
import os
import random
import re
import string
from datetime import datetime

from nltk.tokenize import TweetTokenizer
from nltk.stem.snowball import SnowballStemmer

from sklearn.model_selection import train_test_split

try:
    from textblob import TextBlob
except:
    print("Warning: could not import 'textblob'.",
          "'extended_tweet' function will fail.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=str, help="directory to read from")
    parser.add_argument("-o", "--outfile", type=str,
                        help="Filename to save the results to.",
                        default="tweets")
    parser.add_argument("-f", "--io_function", type=str,
                        help="io function pair to use: text|extended",
                        default="text")
    args = parser.parse_args()
    (read_fn, write_fn) = {
        "text": (text_only, write_tweets_plain),
        "filter_text": (plain_text_filter, write_tweets_plain),
        "extended": (extended_tweet, write_tweets_csv),
        "ext_nodate": (extended_tweet_nodate, write_tweets_csv)
    }[args.io_function]
    print("Extracting tweets...")
    extract_tweets(args.dir, (read_fn, write_fn), args.outfile)


def extract_tweets(directory, io_functions, outfile, file_type=".ndjson"):
    '''Loop through a directory of .ndjson files and perform a given pair of
    read write according to function tuple passed to io_functions param.'''
    tweets = []
    read_fn, write_fn = io_functions
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(file_type):
                continue
            filename = os.path.join(root, f)
            print("reading:", filename)
            for tweet in read_fn(filename):
                tweets.append(tweet)
    train, test = train_test_split(tweets, train_size=0.8, test_size=0.2)
    print("train: {}, test: {}".format(len(train), len(test)))
    write_fn(train, "%s_train" % outfile)
    write_fn(test,  "%s_test" % outfile)


#### functions for reading raw data

def extended_tweet(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if random.random() > 0.5:
                continue # skip half of the rows for now.
            j = json.loads(line)
            body = j["extended_tweet"]
            text = clean(body["full_text"])
            if not isEnglish(text):
                continue
            t = datetime.strptime(j["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
            entities = body["entities"]
            tags = [h["text"] for h in entities["hashtags"]]
            mentioned = [h["screen_name"] for h in entities["user_mentions"]]
            (polarity, subjectivity) = TextBlob(body["full_text"]).sentiment
            yield {"time": t.strftime("%d/%m/%Y %H:%M:%S"),
                   "text": text,
                   "polarity": "{:.4f}".format(polarity),
                   "subjectivity": "{:.4f}".format(subjectivity),
                   "tags": cat(tags),
                   "tag_count": len(tags),
                   "mentioned": cat(mentioned),
                   "mentioned_count": len(mentioned)}

def extended_tweet_nodate(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            text = clean(j["full_text"])
            if not isEnglish(text):
                continue
            entities = j["entities"]
            tags = [h["text"] for h in entities["hashtags"]]
            mentioned = [h["screen_name"] for h in entities["user_mentions"]]
            (polarity, subjectivity) = TextBlob(j["full_text"]).sentiment
            yield {"text": text,
                   "polarity": "{:.4f}".format(polarity),
                   "subjectivity": "{:.4f}".format(subjectivity),
                   "tags": cat(tags),
                   "tag_count": len(tags),
                   "mentioned": cat(mentioned),
                   "mentioned_count": len(mentioned)}

def text_only(filename):
    "return only text of the tweets cleaned"
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            yield clean(json.loads(line)["full_text"])

def plain_text_filter(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                text = json.loads(line)["extended_tweet"]["full_text"]
            except:
                text = json.loads(line)["full_text"]
            if text == "":
                continue
            if "law abiding citizen" in text.lower():
                yield text.replace("\n", "")


#### functions for writing cleaned data to a new file.

def write_tweets_csv(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=data[0].keys())
        w.writeheader()
        for d in data:
            w.writerow(d)
    print("successfully wrote file", filename)
    print("size: {:.2f} MB".format(os.stat(filename).st_size / 1000000.0))

def write_tweets_plain(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for d in data:
            f.write("%s\n" % d)
    print("successfully wrote file", filename)
    print("size: {:.2f} MB".format(os.stat(filename).st_size / 1000000.0))


#### utils

def clean(text, min_len=2):
    '''for a given text input return its cleaned equivalent.
    In this case this means converting to lowercase, stemming,
    filtering out stopwords, digits, links and words shorter
    than the min_len defined.'''
    return cat(stemmer.stem(t) for t in tokenize(text)
               if t not in stopwords
               and not t.startswith("https://")
               and not t.startswith("http://")
               and not t.startswith("@")
               and not t.startswith("#")
               and (len(t) > min_len or t in ("uk","us","eu"))
               and not digit.match(t))

def tokenize(text):
    "Return lowercase tokens generated by the tokenizer"
    return (t.lower() for t in tokenizer.tokenize(text.replace("\n", "")))

def load_stopwords():
    "load stopwords and union with punction sets"
    with open("../resources/stopwords.txt") as sw:
        return (set(w.strip() for w in sw)
                | set(string.punctuation)
                | set("’ .. . “ ” ‘ ...".split()))

def isEnglish(s): return all(ord(c) < 128 for c in s)

tokenizer = TweetTokenizer()
stemmer   = SnowballStemmer("english")
stopwords = load_stopwords()
digit     = re.compile("\d*[,.]\d+|\d+.*")
cat       = " ".join


if __name__ == '__main__':
    main()