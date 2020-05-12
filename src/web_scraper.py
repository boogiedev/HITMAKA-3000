#!/usr/bin/python

# Import Modules
import copy
import numpy as np
import pandas as pd
import os
from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re

# Import Custom Modules
from helpers import *

# Import Credentials
from credentials.keys import *


def scrape_data() -> pd.DataFrame:
    # 2019 Info
    top_songs_2019 = get_top_songs(2019)
    # 2018 Info
    top_songs_2018 = get_top_songs(2018)
    # 2017 Info
    top_songs_2017 = get_top_songs(2017)
    # 2016 Info
    top_songs_2016 = get_top_songs(2016)
    # 2015 Info
    top_songs_2015 = get_top_songs(2015)
    # Year list
    years = [2015, 2016, 2017, 2018, 2019]

    # List of top song tuples by year
    top_songs_list = [top_songs_2015, top_songs_2016, top_songs_2017, top_songs_2018, top_songs_2019]

    # Create DataFrame
    df = pd.DataFrame(
            columns=['song', 'artist', 'featured', 'rank', 'year'],
    )

    # Populate Dataframe
    for year, info in zip(years, top_songs_list):
        x = pd.DataFrame(
            data=[[*info[x], year] for x in range(len(info))],
            columns=['song', 'artist', 'featured', 'rank', 'year'])
        df = df.append(x, ignore_index=True)

    responses, lyrics = [], []
    for song, artist in zip(df['song'], df['artist']):
        res = ""
        try:
            response = get_extract_response(song, artist)
            if not response:
                response = get_extract_response(song, '')
            res = scrape_song_lyrics_from_url(response)
        except:
            pass
        responses.append(response)
        lyrics.append(res)

    # Create Series for each feature
    lyrics_state = pd.Series([response['result']['lyrics_state'] == 'complete' for response in responses]) 
    song_id =  pd.Series([response['result']['id'] for response in responses])
    lyrics_owner_id = pd.Series([response['result']['lyrics_owner_id'] for response in responses])
    primary_artist_url = pd.Series([response['result']['primary_artist']['url'] for response in responses])

    # Create More Features for Each Song ['lyrics_state', 'id', 'lyric_owner_id']
    # Match Lyrics To Song
    df['lyrics'] = pd.Series(lyrics)

    # Match Lyric State To Song
    df['lyrics_state'] = pd.Series(lyrics_state)

    # Match song id To Song
    df['song_id'] = pd.Series(song_id)

    # Match lyric owner To Song
    df['lyrics_owner_id'] = pd.Series(lyrics_owner_id)

    # Match Artist Url To Song
    df['primary_artist_url'] = pd.Series(primary_artist_url)
    
    return df

if '__name__' == __main__:
    # Ask user for path
    print("""Would you like to specify a path: 
*if not specified, output CSV will be in current directory*""")
    path = input()
    print("Scraping Data...")
    data = scrape_data()
    print("\nDone!")
    
    if path:
        data.to_csv(path)
    else:
        cwd = os.getcwd()
        data.to_csv(cwd)