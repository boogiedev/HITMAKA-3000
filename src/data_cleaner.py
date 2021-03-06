#!/usr/bin/python

# Import Modules
import copy
import numpy as np
import nltk
import pandas as pd
from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
import unicodedata
from urllib.parse import urlencode
import re

# Import Custom Modules



def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()


# Create Text Cleaning Function
def clean_text(df:pd.DataFrame, text_field:str, new_text_field_name:str) -> pd.DataFrame:
    df_cop = df.copy()
    cleaned = df_cop[text_field].apply(lambda x: [i.lower() for i in x])
    cleaned = cleaned.apply(lambda line: [re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem) for elem in line])
#     # remove numbers
#     df_cop[new_text_field_name] = df_cop[new_text_field_name].apply(lambda elem: re.sub(r"\d+", "", elem))
    df_cop[new_text_field_name] = cleaned
    return df_cop



def remove_headers(lyrics:str) -> str:
    lyrics = re.sub('(\[.*?\])*', '', lyrics)
    lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
    return lyrics
