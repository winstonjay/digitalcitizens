# -*- coding: utf-8 -*-
'''
Provides basic access to query the guardian's open platform api and
prints results to the stdout.

Example use:
    $ python single.py search -q="facebook" > data.json

For more arg details:
    $ python single.py --help

For api use details:
    http://open-platform.theguardian.com/

NOTE: api key is required for use.
api info: http://open-platform.theguardian.com/
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import argparse

import json
import requests


api_key = os.environ['GUARDIAN_API_KEY']
api_url = 'https://content.guardianapis.com/'

search_roots = ('search', 'section', 'tags', '<single_page_url>')

parser = argparse.ArgumentParser(
    description="Access guardian OP API. prints json results to stdout")
parser.add_argument(
    'domain', type=str, help="type of query eg: %s" % repr(search_roots))
parser.add_argument(
    '-q', '--q', type=str, help="query terms")
# the following will limit results to specific sections or tags.
parser.add_argument(
    '-s', '--section', type=str, help="limit results to section")
parser.add_argument(
    '-t', '--tags', type=str, help="limit results to tags")
args = parser.parse_args()


def build_query(args):
    # setup query url.
    url = "{}{}".format(api_url, args.domain)
    if args.domain not in search_roots:
        # we are doing a single no other querys needed.
        return (url, params)
    # we are searching a colletion, add more params.
    args.domain = None
    for k, param in args.__dict__.items():
        if param and k != 'domian':
            params[k] = param
    return (url, params)

params = {
    'show-fields': 'all',
    'api-key': api_key,
    'show-tags': 'tone,keyword',
    'show-elements': 'all',
    'lang': 'en',
    'page-size': 200,
}



if __name__ == '__main__':
    url, params = build_query(args)
    r = requests.get(url, params=params)

    # just pipe > to file for now because cba.
    print(json.dumps(r.json()))
