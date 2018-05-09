'''
config.py
This file contains all our configuration stuff.
(Not much right now)
'''
import json
import csv

from app.db import Cache

class Options(object):
    '''
    Options is stores application specific information such as file paths for
    data stores.
    '''
    def __init__(self, flags):
        # load the content we want to read.
        try:
            with open(flags.content) as fp:
                self.content = json.load(fp)
        except FileNotFoundError as e:
            raise "Could not load content file: %s" % e

        # load the configuration file that describes our inputs.
        # (essentially our 'code book')
        try:
            with open(flags.book) as fp:
                self.book = list(csv.DictReader(fp))
        except FileNotFoundError as e:
            raise "Could not load code book: %s" % e

        # init our lazy database. This can be empty and a message is printed
        # to the stdout detailing if it has loaded a existing db or created a
        # new one.
        self.db = Cache(flags.db)

        self.DEBUG = True