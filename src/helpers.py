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


problem_lyrics = """I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
If findin' somebody real is your fuckin' problem
Bring your girls to the crib maybe we can solve it
Hold up, bitches simmer down (uh)
Takin' hella long bitch give it to me now (uh)
Make that thing pop like a semi or a nine
Oh, baby like it raw with a shimmy shimmy ya huah
A$AP, get like me
Never met a mother fucker fresh like me
All these motherfuckers wanna dress like me
Put the chrome to your dome make you sweat like Keith
'Cause I'm the nigga, the nigga nigga, like how you figure?
Getting figures and fuckin' bitches
She rollin Swishers, brought her bitches
I brought my niggas, they getting bent up off the liquor
She love my licorice, I let her lick it
They say money make a nigga act nigga-ish
But at least a nigga nigga rich
I be fuckin' broads like I be fuckin' bored
Turn a dyke bitch out have her fuckin' boys, beast
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
If findin' somebody real is your fuckin' problem
Bring your girls to the crib maybe we can solve it
Ooh, I know you love it when this beat is on
Make you think about all of the niggas you've been leading on
Make me think about all of the rappers I've been feeding on
Got a feeling that's the same dudes that we speakin' on, oh word?
You ain't heard my album? Who you sleepin' on?
You should print the lyrics out and have a fucking read-along
Ain't a fucking sing-along 'less you brought the weed along
Then ju' (okay, I got it) then just drop down and get your eagle on
Or we can stare up at the stars and put The Beatles on
All that shit you talkin' 'bout is not up for discussion
I will pay to make it bigger I don't pay for no reduction
If it's comin' from a nigga I don't know, then I don't trust it
If you comin' for my head, then mothafucka' get to bustin'
Yes Lord, I don't really say this often
But this long dick nigga ain't for the long talkin', I beast
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
If findin' somebody real is your fuckin' problem
Bring your girls to the crib maybe we can solve it
Uh, yeah, hoe this the finale
My pep talk turn into a pep rally
Say she's from the hood but she live inside in the Valley now
Vacate in Atlanta, then she going back to Cali, mmm
Got your girl on my line, world on my line
The irony I fuck 'em at the same damn time
She eyein' me like a nigga don't exist
Girl, I know you want this dick
Girl, I'm Kendrick Lamar, mmm
A.K.A. Benz is to me is just a car, mmm
That mean your friends need to be up to par
See my standards are papered by threesomes tomorrow, mmm
Kill 'em all dead bodies in the hallway
Don't get involved listen what the crystal ball say
Halle Berry, hallelujah
Holla back I'll do ya, beast
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
I love bad bitches that's my fuckin' problem (problem)
And yeah, I like to fuck I got a fuckin' problem (true)
If findin' somebody real is your fuckin' problem
Bring your girls to the crib maybe we can solve it, ay"""