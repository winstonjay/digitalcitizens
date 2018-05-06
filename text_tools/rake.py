# -*- coding: utf-8 -*-
'''rake.py:

Derivation of R.A.K.E (rapid automatic keyword extraction) algorithm as
described in:
    Rose, S. Engel, D. Cramer, N. and Cowley, W. 2010.
    Automatic keyword extraction from individual documents
    https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents

This algorithm needs stopwords and punctuation to be present within the data.
'''
from __future__ import division
from __future__ import print_function

import re
import collections
import operator



class KeywordExtractor(object):
    '''KeywordExtractor class implements an methods derived from the RAKE
    (Rapid automatic Keyword Extraction) algorithm to provide ways of quickly
    generating keywords from individual documents.'''
    def __init__(self, stop_words, phase_lim='.,?!:;'):
        self.stop_words  = stop_words
        self.stop_tokens = stop_words | set(phase_lim)
        # set word splitting pattern for extracting candidates
        pattern = '(?:[A-Z][\.-])+|\w+|[{}]'.format(re.escape(phase_lim))
        self.regex = re.compile(pattern)

    def keywords(self, document):
        "return a sorted list of keywords"
        try:
            return next(zip(*self.extract_keywords(document)))
        except:
            return []

    def extract_keywords(self, document):
        "return a sorted list of keyword, score tuples"
        scores = self.all_scores(document)
        T = len(scores) // 3
        return sorted(scores, key=index(1), reverse=True)[:T]

    def all_scores(self, document):
        "return a list scores for all phrases"
        uniq = set()
        freq = collections.defaultdict(int)
        degs = collections.defaultdict(int)
        for phrase in self.__extract_phrases(document):
            uniq.add(phrase)
            words = phrase.split()
            for w in words:
                freq[w] += 1
                degs[w] += len(words)
        return [(k, self.__phrase_score(k, degs, freq)) for k in uniq]

    ####### keyword score calculation

    def __phrase_score(self, k, degs, freq):
        "compute sum of deg(w) / freq(w) for each word in a phrase"
        return sum((degs[w]) / freq[w] for w in k.split())

    def candidates(self, document):
        "return a set all posible candidates"
        return set(self.__extract_phrases((document)))

    def __extract_phrases(self, document):
        "return a generator that emits candidate phrases."
        phrase = []
        for w in self.regex.findall(document.lower()):
            if w in self.stop_tokens:
                if phrase and is_valid(phrase):
                    yield concat(phrase)
                phrase = []
            else:
                phrase.append(w)
        if phrase and is_valid(phrase):
            yield concat(phrase)

    def adjoin(self, keywords):
        # look through the document to find keywords that should be joined
        # up. That is if a stopword has split them on more than one occasion
        # the example that is given is 'axis (of) evil'.
        # its score shall be the sum of its constituent scores.
        pass


#### some helper functions

def is_valid(phrase):
    "return if a phrase is a valid keyword"
    # TODO: This is a make do solution for now.
    text = concat(phrase)
    return (not concat(phrase).isdigit() and
            text not in ignore_terms and
            (len(text) > 3 or text[0].isupper()))

index  = operator.itemgetter
concat = ' '.join

ignore_terms = ("day", "year", "last", "years", "first")




####### Finding the top keywords in the collection.
#
# Some additional mesures described in the paper:
#
# refereneced document frequency: rdf(k) = how many documents a candidate
# keyword has appeared in.
#
# extraction document frequency: edf(k) = how many documents a keyword has
# been extracted from.
#
# exclusiveness: exc(k) = edf(k) / rdf(k)
# essentialness: ess(k) = exc(k) * edf(k)
# genrality:     gen(k) = rdf(k) * (1.0 - exc(k))
#
# the paper describes:
# 'Keywords that are both highly essential and highly general are essential
# to a set of documents within the corpus but also referenced by a
# significantly greater number of documents within the corpus than other
# keywords.'
#
# Question is how to return the highly essential and highly general. sh
#
#   collection_score(k) = ???
#
#
class CollectionOperator(object):
    '''CollectionOperator implements methods to describe a collection of
    documents using'''
    def __init__(self, extractor, docs=[]):
        self.extractor = extractor
        self.docs = docs

    def add(self, document):
        "add document to the collection"
        self.docs.append(document)

    # NOTE prehaps vecorization would be better here the formulas described in
    # the paper all work with the features generated by reference document
    # frequency and extraction document freqency.
    def fit(self, docs=[]):
        if not docs and not self.docs:
            print("No data provided returning empty dict")
            return {}
        rdf = collections.defaultdict(int)
        edf = collections.defaultdict(int)
        for doc in self.docs:
            for k in self.extractor.keywords(doc):
                edf[k] += 1
            for k in self.extractor.candidates(doc):
                rdf[k] += 1
        scores = {}
        for k in rdf:
            # values are left in even though some are not used. This is to
            # remind of the feature set that we can work with. TODO.
            exc = edf[k] / rdf[k]
            ess = exc * edf[k]
            gen = rdf[k] * (1.0 - exc)
            # Still not clear what the ideal function is to perform.
            # this seems very depended on the use case.
            scores[k] = ess # * gen
        return scores