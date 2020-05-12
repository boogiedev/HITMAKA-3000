#!/usr/bin/python

# Import Modules
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re

# Import Credentials
from credentials.keys import *

# Set API Payload
base_url = 'https://api.genius.com/search'
headers = {'Authorization': 'Bearer ' + client_token}

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    path = song_api_path
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics

def jsonReader(jsonFile):
    try:
        for key, value in jsonFile.items():
            print(f"|KEY:{key} | VALUE:{value}\n")
    except:
        print("Input is not a JSON/DICT object")

def request_song_info(song_title, artist_name):
    data = {'q': f"{song_title} {artist_name}"}
    response = requests.get(base_url, data=data, headers=headers)
    return response.json()


def get_full_lyrics(song:str='', artist:str=''):
    if not song and artist:
        song = input("Enter a song: ")
        artist = input("Enter the artist: ")

    "DATA OBJECTS"
    # JSON/DICT Object
    api_test = request_song_info(song, artist)
    # JSON/DICT Object
    api_testReponse = api_test["response"]
    # LIST Object
    api_responseHits = api_testReponse["hits"]
    # JSON/DICT Object
    main_info = api_responseHits[0]
    # JSON/DICT Object
    main_info_result = main_info["result"]

    # API Paths
    song_api_path = main_info_result["api_path"]

    # Music Data
    lyric_url_path = main_info_result["path"]
    title = main_info_result["title"]
    featured_artists = main_info_result["title_with_featured"]
    full_lyrics = lyrics_from_song_api_path(song_api_path)

    return full_lyrics


def get_top_songs(year:int, partition_artist=True) -> list:
    '''Returns TOP 50 Rap Songs for given year'''
    # Set Scrape URL
    url = 'https://www.billboard.com/charts/year-end/%s/hot-rap-songs'

    song_class = 'ye-chart-item__title'
    artist_class = 'ye-chart-item__artist'
    rank_class = 'ye-chart-item__rank'

    # Request URL
    response = requests.get(url % str(year))

    # Create Beautiful Soup Object
    soup = BeautifulSoup(response.content, "html.parser")

    # Find All Divs with Song Title
    song_dump = soup.findAll("div", {"class": song_class})
    # Find All Divs with Artist name
    artist_dump = soup.findAll("div", {"class": artist_class})
    # Find All Divs with Song Rank
    rank_dump = soup.findAll("div", {"class": rank_class})

    # Derive Song titles from song_dump
    songs = [entry.get_text(strip=True) for entry in song_dump]
    # Derive Artist names from artist_dump
    artists = [entry.get_text(strip=True) for entry in artist_dump]
    # Derive Song Ranks from rank_dump
    rankings = [entry.get_text(strip=True) for entry in rank_dump]
    
    if partition_artist:
        artists = [x.partition('Featuring')[0] for x in artists]
        featured = [x.partition('Featuring')[2] for x in artists]

    return list(zip(songs, artists, featured, rankings))
    
    
def get_extract_response(title:str, artist:str) -> dict:
    search_term = "{s} {a}".format(s=title, a=artist).strip()
    endpoint = "search/multi?"
    params = {'per_page': 1, 'q': search_term}

    # This endpoint is not part of the API, requires different formatting
    url = "https://genius.com/api/" + endpoint + urlencode(params)
    res = requests.get(url)
    response = res.json()['response'] if res else None
    try:
        return response['sections'][0]['hits'][0]
    except:
        return None
    
    
def scrape_song_lyrics_from_url(response:str, remove_section_headers=True) -> str:
    """ Use BeautifulSoup to scrape song info off of a Genius song URL
    :param url: URL for the web page to scrape lyrics from
    """
    if response['result']:
        url = response['result']['url']
    else:
        return None
    page = requests.get(url)
    if page.status_code == 404:
        return None

    # Scrape the song lyrics from the HTML
    html = BeautifulSoup(page.text, "html.parser")
    div = html.find("div", class_="lyrics")
    if not div:
        return None # Sometimes the lyrics section isn't found

    # Scrape lyrics if proper section was found on page
    lyrics = div.get_text()
    if remove_section_headers:  # Remove [Verse], [Bridge], etc.
        lyrics = re.sub('(\[.*?\])*', '', lyrics)
        lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
    return lyrics.strip("\n")



