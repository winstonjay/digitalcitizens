# -*- coding: utf-8 -*-
'''
chain.py

Generate psuedo-random chains of text.

usage: chain.py [-h] [-l LEN] [-n NUMBER] [-k SAMPLES] [-s SEED] [-f FILE]

Reference: https://golang.org/doc/codewalk/markov/
'''
import sys
import random
import argparse
from collections import defaultdict


def main():
    args = parse_args()
    f = sys.stdin if not args.file else open(args.file)
    c = Chain(args.number)
    c.build(read_file(f))
    for _ in range(args.samples):
        print(c.generate(args.len, seed=args.seed))


class Chain(object):
    '''Chain contains a dict ("chain") of prefixes to a list of suffixes.
    A prefix is a string of prefixLen words joined with spaces.
    A suffix is a single word. A prefix can have multiple suffixes.'''
    def __init__(self, n=3):
        self.n = n
        self.chain = defaultdict(list)

    def build(self, iterable):
        '''Build reads text from the provided file_reader and parses it into
        prefixes and suffixes that are stored in Chain. A file reader is a
        iterator that emits tokens to be stored in the chain.'''
        prefix = [""] * self.n
        for s in iterable:
            self.chain[cat(prefix)].append(s)
            prefix = prefix[1:] + [s]

    def generate(self, text_len, seed=None):
        "generate returns a string of at most n words generated from Chain."
        seed = seed or random.choice(list(self.chain))
        seed = seed.split()
        prefix = seed[-self.n:]
        assert len(prefix) >= self.n, "Seed too short >=%d" % self.n
        return self._generate(text_len, seed, prefix)

    def _generate(self, text_len, words, prefix):
        "_generate executes the chain generation with properly prepared args"
        for _ in range(text_len):
            choices = self.chain[cat(prefix)]
            if not choices:
                break
            s = random.choice(choices)
            words.append(s)
            prefix = prefix[1:] + [s]
        return cat(words)


#### Helper functions

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate psuedo-random chains of text.")
    parser.add_argument('-l', '--len',
        type=int, help='Chain prefix len', default=3)
    parser.add_argument('-n', '--number',
        type=int, help='Est number of words to generate', default=15)
    parser.add_argument('-k', '--samples',
        type=int, help='Number of samples to generate', default=1)
    parser.add_argument('-s', '--seed',
        type=str, help='start seed for text.')
    parser.add_argument('-f', '--file',
        type=str, help='Input file.')
    return parser.parse_args()

def read_file(file):
    "emit file contents delimted by whitespace"
    for line in file:
        for word in line.split():
            yield word.lower()

cat = " ".join

if __name__ == '__main__':
    main()