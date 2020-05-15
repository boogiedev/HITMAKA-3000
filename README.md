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


# HITMAKA INDUSTRIES 

Are you an aspiring SoundCloud rapper? Are you tired of spamming clickbait comments on social media to gain views? 

Well fear no more, HITMAKA Industries is here to help you. We gurantee that your rap career will blow up if you use our newest invention, the HITMAKA3000! Using advanced Machine Learning techniques, we have created a Natural Language Processor that has analyzed the lyrics of all the TOP rap songs in the last 10 years! This has given us KEY insights as to what makes a rap song lyrically hot! Our HITMAKA3000 will provide you with all the things you need to lyrically make the next hottest hit! 

It will help you with:
- Name Dropping
- Theme
- Flexmeter (Patented)
- AD LIBZ (beta testing)

You're now wondering HOW we were able to do all of this? Let us show you...


## Basic Overview

### Context

### Goal

## Exploring Data

SOURCES             | TYPE | METRIC
:-------------------------:|:-------------------------:|:-------------------------:|
[BILLBOARD YEAR-END CHARTS](https://www.billboard.com/charts/year-end/2019/hot-r-and-and-b-hip-hop-songs)  | Top Charts |  2010-2020
[GENIUS API](https://docs.genius.com/)  | Lyrics |  *




### Web Scraping



### Initial Intake

Just found out that the data that I scraped is flawed, from 2000-2013, the billboard website is glitched and are reporting the same songs for those 13 years.

Here is a detailed description of the intake data:
- `ID`: Report ID

<p align="center">
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/"></img>
</p>



### Visualizations


[Pre LDA Report](https://boogiedev.github.io/HITMAKA-3000/lda.html)
[Post LDA Report](https://boogiedev.github.io/HITMAKA-3000/post_lda.html)

#### LDA Results

```
Topics found via LDA:

Topic #0:
expletive_0 love uh expletive_1 woo expletive_6 baby man money expletive_3 skrrt drop thun cardi bad

Topic #1:
expletive_3 expletive_1 expletive_0 expletive_4 baby love right cause time say god real tell want better

Topic #2:
gang gucci watch lil wicked drake cut love west kanye bust expletive_3 bop expletive_1 young

Topic #3:
hitta hittas love lil 2016 money black expletive_3 young ring saying rake world rich mask

Topic #4:
expletive_0 expletive_1 walk expletive_3 want love nothin talk money bout feel ball bank taste young

Topic #5:
expletive_0 expletive_3 expletive_4 hol really expletive_1 look want man em say cause money keys feel

Topic #6:
expletive_0 expletive_1 expletive_3 baby want expletive_4 hit love pop right expletive_2 ta girl cause money
```

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

- Flexmeter 

## License
[MIT ©](https://choosealicense.com/licenses/mit/)

