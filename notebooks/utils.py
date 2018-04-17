# -*- coding: utf-8 -*-
'''
utils.py

Some generic utilites for use within the notebooks.
'''
from __future__ import print_function

import sys

# Make imports from the text_tools folder eaiser so we dont have to do
# something like this or think about complicated import paths every time.
sys.path.append('../text_tools')

# _includes path to write html/md to noted here to make access easier.
page_path = '../../gh-pages/_includes/'


#### Functions

concat = ' '.join

def fprintf(f, text, *args, **kwargs):
    "fprintf with python format formating"
    print(text.format(*args, **kwargs), file=f)

def printf(string, *args, **kwargs):
    "printf with python format formating"
    print(string.format(*args, **kwargs))