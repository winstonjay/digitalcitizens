# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import zipfile
import json
import re


def write_data(filename, outfilename):
    "read first "
    outfile = open(outfilename, mode="w+")
    print("Started writing to file:", outfilename)
    i = 0
    with zipfile.ZipFile(filename) as z:
        for fn in z.namelist()[1:]:
            print("reading:", fn)
            with z.open(fn) as f:
                for line in f:
                    t = extract_line(line)
                    if t:
                        print(t, file=outfile)
                        i += 1
    outfile.close()
    print("Finished writing to file:", outfilename)
    print("Total tweets:", i)


def extract_line(line):
    '''clean_line converts the text to lowercase remove all non words,
    stopwords, non ascii characters and links and groups all corpora specfic
    terms so that they will be processed as one entity. Eg: Hello World ->
    hello_world.'''
    s = json.loads(line)["extended_tweet"]["full_text"]
    if not s or not is_ascii(s):
        return None
    s = re.sub(r'[^\x00-\x7F]+|\n|http\S+', ' ', s.lower())
    if not s.strip():
        return None
    return cat(w for w in rx.findall(s)
                if 3 < len(w) < 20
                if w not in stop_words)

cat = " ".join

rx = re.compile(r"[#@]\w+|\w+")

stop_words = set(open("../resources/stopwords.txt").read().split())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="input filename", required=True)
    parser.add_argument(
        "-o", "--out", type=str, help="output filename", required=True)
    args = parser.parse_args()

    # perform all ops
    write_data(args.file, args.out)