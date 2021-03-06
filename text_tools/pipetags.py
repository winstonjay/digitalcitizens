# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import zipfile
import json
import re


def write_data(filename, outfilename):
    "Read and write out all tweet tags line by line"
    outfile = open(outfilename, mode="w+")
    with zipfile.ZipFile(filename) as z:
        # read file by file of zip archive skiping the first dir path.
        for fn in z.namelist()[1:]:
            print("reading:", fn)
            with z.open(fn) as f:
                for line in f:
                    tags = extract_tag(line)
                    if tags:
                        print(tags, file=outfile)
    outfile.close()
    print("Finished writing to file:", outfilename)

def extract_tag(line):
    "gets tags tweet by tweet returning their names seperated by spaces."
    tags = json.loads(line)["extended_tweet"]["entities"]["hashtags"]
    return cat(t['text'] for t in tags)


cat = " ".join

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="input filename", required=True)
    parser.add_argument(
        "-o", "--out", type=str, help="output filename", required=True)
    args = parser.parse_args()

    write_data(args.file, arges.out)