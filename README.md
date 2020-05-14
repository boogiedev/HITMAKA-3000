![HITMAKA HEADER](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/hitmaka30.gif)
> An exploration of the hip-hop music industry and what it lyrically takes to gain traction

<p align="center">
  <img src="https://img.shields.io/badge/Maintained%3F-IN PROG-green?style=flat-square"></img>
  <img src="https://img.shields.io/github/commit-activity/m/boogiedev/HITMAKA-3000?style=flat-square">
</p>


## Table of Contents

- [Basic Overview](#basic-overview)
  - [Context](#context)
  - [Goal](#goal)
- [Exploring Data](#exploring-data)
  - [Web Scraping](#web-scraping)
  - [Initial Intake](#initial-intake)
- [Language Processing](#language-processing)
  - [Tokenizing](#tokenizing)
  - [Visualizations](#visualizations)
- [**K O D A K  B O T  3 0 0 0**](#k-o-d-a-k--b-o-t--3-0-0-0)
- [Future Considerations](#future-considerations)
- [License](#license)


## Basic Overview

### Context

### Goal

## Exploring Data

SOURCES             | TYPE | METRIC
:-------------------------:|:-------------------------:|:-------------------------:|
[BILLBOARD YEAR-END CHARTS](https://www.billboard.com/charts/year-end/2019/hot-r-and-and-b-hip-hop-songs)  | Top Charts |  2015-2020
[GENIUS API](https://docs.genius.com/)  | Lyrics |  *




### Web Scraping



### Initial Intake

Here is a detailed description of the intake data:
- `ID`: Report ID

<p align="center">
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/"></img>
</p>



### Visualizations

---

# K O D A K  B O T  3 0 0 0

#### Scrape Lyrics

In order to get started in making the ***K O D A K  B O T  3 0 0 0***, I used the [GENIUS API](https://docs.genius.com/), as well as a library [LyricsGenius](https://github.com/johnwmillr/LyricsGenius) that helps in scraping the data. 

<p>
  <img align="right" src="https://gifimage.net/wp-content/uploads/2018/04/kodak-black-gif-6.gif"></img>
</p>

```python
# Set Target Artist
trg_artist = 'Kodak Black'
# Create API Instance
api = genius.Genius(client_token)
# Search Artist Information
artist = api.search_artist(trg_artist)
```

When scraping for all of Kodak's songs, we ended up with a total of 267 songs, the sample data in table below is truncated.

NUM            | SONG | 
:-------------------------:|:-------------------------:|
Song 1 | "Tunnel Vision"
Song 2 | "No Flockin"
Song 3 | "Roll in Peace"
Song 4 | "ZEZE"
Song 5 | "SKRT"


#### Lyric Format

After scraping the lyrics, we now have to access the JSON data and pull out the individual lyrics per song, let's take a look at the structuing of the JSON file.

<p >

```python
# Save Lyrics from Artist
aux = artist.save_lyrics(filename='lyrics.json', overwrite=True, verbose=True)
```

  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/kodakscrape.PNG" width='80%'></img>
</p>

#### Cleaning 

Sample of pre-clean tokens from NLTK *word_tokenize* function
```python
['glee', 'southside', 'ayy', ',', 'lil', 'metro', 'beat', 'lil', 'kodak', ',', 'dont', 'like', 
'see', 'winnin', 'wan', 'na', 'see', 'penitentiary', 'need', 'lil', 'baby', 'gon', 'listen',
'girl', ',', 'dont', 'wan', 'na', 'one', 'iggin']
```
It seems like with the NLTK module, some of the slang and informal spelling of words become chopped up... looks like we have to make our own tokenizer!

```python
['glee', 'southside', 'ayy', 'lil', 'metro', 'on', 'that', 'beat', 'lil', 'kodak', 'they', 'dont', 'like', 
'to', 'see', 'you', 'winnin', 'they', 'wanna', 'see', 'you', 'in', 'the', 'penitentiary', 'i', 'need', 'me', 
'a', 'lil', 'baby', 'who', 'gon', 'listen', 'girl', 'i', 'dont', 'wanna', 'be', 'the', 'one', 'you', 'iggin']
```

This looks so much better!



## Future Considerations

## License
[MIT ©](https://choosealicense.com/licenses/mit/)

