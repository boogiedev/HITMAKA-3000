#!/usr/bin/python

# Import Modules
import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

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


def get_top_songs(year:int) -> list:
    # Set Scrape URL
    url = 'https://www.billboard.com/charts/year-end/%s/hot-r-and-and-b-hip-hop-songs'

    song_class = 'ye-chart-item__title'
    artist_class = 'ye-chart-item__artist'
    
    # Request URL
    response = requests.get(url % str(year))
    
    # Create Beautiful Soup Object
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find All Divs with Song Title
    song_dump = soup.findAll("div", {"class": song_class})
    # Find All Divs with Artist name
    artist_dump = soup.findAll("div", {"class": artist_class})
    
    # Derive Song titles from song_dump
    songs = [entry.get_text(strip=True) for entry in song_dump]
    # Derive Artist names from artist_dump
    artists = [entry.get_text(strip=True) for entry in artist_dump]
    
    return list(zip(songs, artists))
    
    