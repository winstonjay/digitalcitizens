# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from datetime import datetime
import json
import re
import os
import zipfile

from spamfilter import HashtagSpamFilter


def writer(filename, out_filename, spam_filter):
    '''read zip archive of .ndjson files and write to a single file then
    compress into a new zip archieve.'''
    # set up scoped function varibles
    i = 0
    tmp_filename = out_filename
    with open(tmp_filename, "w") as tmp_file:
        print("Started writing to file:", tmp_filename)
        with zipfile.ZipFile(filename) as z:
            for fn in z.namelist()[1:]:
                print("reading:", fn)
                with z.open(fn) as f:
                    for line in extract_tweets(f, spam_filter):
                        print(line, file=tmp_file)
                        i += 1
    # log result
    print("Finished writing to file:", tmp_filename)
    print("Total tweets:", i)
    print("spam percent=", (spam_filter.x / i) * 100)
    print("compressing file...")

    # compress tmp file into local zip.
    z_filename = out_filename + ".zip"
    with zipfile.ZipFile(z_filename, "w") as z:
        z.write(tmp_filename, compress_type=zipfile.ZIP_DEFLATED)
    print("wrote to file", z_filename)
    # clean up
    print("cleaning up uncompressed file", tmp_filename)
    os.remove(tmp_filename)


def extract_tweets(f, spam_filter):
    "extract tweet created_at, tags and text from each tweet json object."
    for line in f:
        t = json.loads(line)
        tags, tags_n = extract_hashtags(t["extended_tweet"]["entities"])
        if spam_filter.filter_tags(tags, tags_n):
            continue
        text = extract_text(t["extended_tweet"]["full_text"])
        if not text:
            continue
        time = datetime.strptime(t["created_at"], time_read)
        time_str = time.strftime(time_write)
        yield tab([time_str, text, tags or "null"])
    print(spam_filter.stats())


tab = "\t".join
time_read  = "%a %b %d %H:%M:%S +0000 %Y"
time_write = "%d/%m/%Y %H:%M:%S"


def extract_text(text):
    '''clean_line converts the text to lowercase remove all non words,
    stopwords, non ascii characters and links and groups all corpora specfic
    terms so that they will be processed as one entity. Eg: Hello World ->
    hello_world.'''
    s = re.sub(r'[^\x00-\x7F]+|\n+|http\S+', ' ', text.lower().replace("\n", "")
        ).replace("cambridge analytica", "cambridge_analytica"
        ).replace("mark zuckerberg", "mark_zuckerberg")
    return cat(w for w in rx.findall(s)
                if 3 < len(w) < 20
                if w not in stop_words)


rx = re.compile(r"[#@]\w+|\w+")

cat = " ".join

stop_words_path = "../resources/stopwords.txt"
stop_words = set(open(stop_words_path).read().split())


def extract_hashtags(entities):
    "gets tags tweet by tweet returning their names seperated by spaces."
    tags = [t['text'] for t in entities["hashtags"]]
    n = len(tags)
    tags = cat(tags)
    return (tags, n) if n < 10 and is_ascii(tags) else (None, -1)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)


if __name__ == '__main__':
    # io params
    filename  = "raw/fb_ca_march.zip"
    outfile   = "tweet01.tsv"
    spam_filter = HashtagSpamFilter()

    # do your thang
    writer(filename, outfile, spam_filter)