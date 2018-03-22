'''
chain.py

Reference: https://golang.org/doc/codewalk/markov/
'''
import sys
import random
from collections import defaultdict


def main():
    c = Chain()
    c.build(read_file(sys.stdin))
    seed = random.choice(c.chain.keys())
    print(c.generate(10, seed))


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

    def generate(self, text_len, seed):
        "Generate returns a string of at most n words generated from Chain."
        words = [seed]
        prefix = seed.split()
        for _ in range(text_len):
            choices = self.chain[cat(prefix)]
            if not choices:
                break
            s = random.choice(choices)
            words.append(s)
            prefix = prefix[1:] + [s]
        return cat(words)


#### Helper functions

def read_file(file):
    "emit file contents delimted by whitespace"
    for line in file:
        for word in line.split():
            yield word.lower()

cat = " ".join

if __name__ == '__main__':
    main()