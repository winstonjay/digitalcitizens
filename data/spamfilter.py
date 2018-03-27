# -*- coding: utf-8 -*-

# TODO: this is a bit of a quick fix for now. If needed in the future
# work out a better strategy and refine implementation.

'''Performs basic spam filtering on tweets using hashtag frequencies.'''

import collections

class HashtagSpamFilter(object):
    '''keep track of frequently occuring lists of hashtags, for tweets with a
    given minimum number of hashtags. If the number of ouccuracnes reaches a
    given threshold we will say that all any more that occur are spam.'''

    def __init__(self, max_tags=10, theta=4, threshold=20):
        self.maybe_spam = collections.Counter()
        self.spam = set()
        self.max_tags = max_tags
        self.theta = theta
        self.threshold = threshold
        self.x = 0

    def filter_tags(self, tags, tags_n):
        # if the tag count is too high its probally spam.
        # currently the tag extracter returns -1 for too long tags
        # fix this in the future the resposibility doesent make sense.
        if tags_n == -1 or tags in self.spam:
            self.x += 1
            return True
        # if the tag count is high and the frequency of these tags within
        # the collection is unaturally high filter all future occurances.
        if tags_n > self.theta:
            if self.maybe_spam[tags] > self.threshold:
                del self.maybe_spam[tags]
                self.spam.add(tags)
                self.x += 1
                return True
            self.maybe_spam[tags] += 1
        return False

    def stats(self):
        "return some printable stats to monitor."
        return ("spam_sets={} | maybe_spam={} | spam={}".format(
                len(self.spam), len(self.maybe_spam), self.x))