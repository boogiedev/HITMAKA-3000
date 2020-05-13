#!/usr/bin/python

# Import Modules
from collections import Counter
import numpy as np
import pandas as pd
import json
from pprint import pprint
import string
from math import log
import re



def match_dummies(item:str):
    """Replaces profanity with dummy word"""
    bad_prefixes = ['nig', 'bitc', 'puss', 'fuc', 'shit', 'hoe', 'ass', 'cock', 'fag', 'tits', 'cunt', 'dick', 'piss']
    replace_prefixes = ['nibba', 'binch', 'boos', 'duck']
    for pre, rep in zip(bad_prefixes, replace_prefixes):
        match = r'({bad_prefix})(.*?)\b'.format(bad_prefix=pre)
        res = re.sub(match, rep, sentence)
        print(res)