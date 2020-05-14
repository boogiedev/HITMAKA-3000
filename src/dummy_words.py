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
import matplotlib.pyplot as plt
import seaborn as sns


def match_dummies(item:str):
    """Replaces profanity with dummy word"""
    bad_prefixes = ['nig', 'bitc', 'puss', 'fuc', 'shit', 'hoe', 'ass', 'cock', 'fag', 'tits', 'cunt', 'dick', 'piss']
    replace_prefixes = [f"expletive_{i}" for i in range(len(bad_prefixes))]
    for pre, rep in zip(bad_prefixes, replace_prefixes):
        match = r'({bad_prefix})(.*?)\b'.format(bad_prefix=pre)
        item = re.sub(match, rep, item)
    return item

# Helper function
def plot_10_most_common_words(count_data, count_vectorizer, title:str='10 most common words'):
    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts+=t.toarray()[0]
    
    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x:x[1], reverse=True)[0:10]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words)) 
    
    plt.figure(2, figsize=(15, 15/1.6180))
    plt.subplot(title=title)
    sns.set_context("notebook", font_scale=1.75, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90) 
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.show()
    
# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))