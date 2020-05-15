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
  - [Text Cleaning](#text-cleaning)
  - [Visualizations](#visualizations)
- [Topic Modeling](#topic-modeling)
  - [Latent Dirichlet Allocation](#latent-dirichlet-allocation)
- [**K O D A K  B O T  3 0 0 0**](#k-o-d-a-k--b-o-t--3-0-0-0)
- [Future Considerations](#future-considerations)
- [License](#license)

<details>
  <summary>
    Business Context
  </summary>
  
  
# HITMAKA INDUSTRIES 

***Are you an aspiring SoundCloud rapper? Are you tired of spamming clickbait comments on social media to gain views?***

- Well fear no more, HITMAKA Industries is here to help you. We gurantee that your rap career will blow up if you use our newest invention, the **HITMAKA3000**!


- Using advanced *Machine Learning* techniques, we have created a Natural Language Processor that has analyzed the lyrics of all the TOP rap songs in the last 10 years!


- This has given us **KEY** insights as to what makes a rap song lyrically hot! Our **HITMAKA3000** will provide you with all the things you need to lyrically make the next hottest hit! 

It will help you with:
- Name Dropping
- Theme
- Flexmeter (Patented)
- AD LIBZ (beta testing)

You're now wondering HOW we were able to do all of this? Let us show you...



</details>



## Basic Overview

Natural Language Processing (NLP) is the act of using software to process speech and text, etc. This is possible with Machine Learning, having computers parse through text in an attempt to derive meaning from how we as humans express ourselves. As you may infer, there are a lot of nuances with written languages, and even more so with each specific one. Today, we are looking at processing text from the English language, more namely, rap lyrics.  

### Context


<p >
  <img  align="right" width="40%" src="https://thumbs.gfycat.com/SparklingFlatIslandwhistler-size_restricted.gif"></img>


In an attempt to process the language of rap music, there are a lot of problems that arise. The prose, dictation, play on words, ad-libs, onomatopeias and other idiosyncrasies that appear in rap are hard for NLP tasks, as the tooling for this are mainly geared towards more formal and "proper" speech in terms of grammar. 

</p>

</br></br>

For a machine to process a sentence like this:
  > *"Jane went to the store today and bought bananas"*

There are distinct parts of speech that can be broken down.

The above example as opposed to this below will yeild different results:
  > *"I'm pulling up in that Bruce Wayne but I'm the ####ing villain"*


### Goal

The original goal of this project was to use NLP techniques, combined with Neural Netowrks in order to gain insight as to ***What makes a hit rap song?***. Althought this is a generally broad question (since rap music cannot be boiled down to simply words), the idea was to source the top 100 rap songs from each year and using the NLTK suite, find thematic elements, common trends, and the top words that were prevalent in the top songs.

**TLDR**:
The goal of this project ended up shifting into *unsupervised* **TOPIC MODELING** rather than a discrete prediction value. 
The main blockage that led to this ended up being very insightful to my understanding of the NLP field. 


---

## Exploring Data

NUM  |  SOURCES             | TYPE | METRIC
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
1 | [BILLBOARD YEAR-END CHARTS](https://www.billboard.com/charts/year-end/2019/hot-r-and-and-b-hip-hop-songs)  | Top Charts |  2010-2020
2 | [GENIUS API](https://docs.genius.com/)  | Lyrics |  *

<p align="center">
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/bill_board.gif"></img>
</p>

</br>

<p align="center">
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/genius_api.gif"></img>
</p>


### Web Scraping

After finding where I wanted to source my data from, I wrote a program to automatically find and parse the top songs from the years 2010-2020 as well as find the lyrics, artist, and other meta-data that belonged to each song. 


<details>
  <summary>
    Scraping Functions
  </summary>
  
  
```python
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
```

</details>



### Initial Intake

When the scraping was finished, I translated all of the information I needed into a data-frame and then exported it to a CSV for future use.

<p align="center">
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/intakedata.PNG"></img>
</p>

Here is a detailed description of the intake data:
- `song`: Song Name
- `artist`: Artist Name
- `featured`: Featured Artist Names
- `rank`: Song Ranking
- `year`: Chart Year
- `lyrics`: Song Lyrics
- `lyrics_state`: Lyrics State (if lyrics were complete)
- `song_id`: Song ID on GeniusAPI 
- `lyrics_owner_id`: Lyric Owner ID
- `primary_artist_url`: Primary Artist's GeniusAPI URL Endpoint (if needed to backtrack)


*Note*
> Just found out that the data that I scraped is flawed, from 2000-2013, the billboard website is glitched and are reporting the same songs for those 13 years.

## Language Processing

### Text Cleaning

The standard text-cleaning procedure was used to process the lyric data.

The following was removed/changed:
- Punctuation
- Lyric Headers
- Casing (standardized to lowercase)
- Replace expletives with codes
- Remove Stop Words (standard NLTK 'english', later revised to custom stop words)

custom_stop = ['im', 'thats', 'ya', 'though', 'yeah', 'like', 'got', '2018', 'know', 'get', 'aint', 'ayy', 'go', 'na', 'back', 'one', 'gon', 'make', 'wan', 'thats', 'need', 'oh', 'see', 'feat', 'ooh', 'said', 'way', "2017", "la", 'lets', 'ft', 'let', 'hey', 'ima', 'uoeno', 'oohoohoohooh', 'ah', 'js', 'pare']


#### Attempt to Stem/Lemmatize

<details >
  <summary>
    Stemming/Lemmatize Functions
  </summary>


```python
# Create Porter, Snowball, WordNet Objects
porter = PorterStemmer()
snowball = SnowballStemmer('english')
wordnet = WordNetLemmatizer()

# Get functions from each object
porter_func = porter.stem
snowball_func = snowball.stem
wordnet_func = wordnet.lemmatize

# Create lambda func to easily apply func to each token
get_root = lambda tokens, func: [func(token) for token in tokens] 

# Get Tokens for each type of processor
porter_tokens = data['tokens'].apply(lambda x: get_root(x, porter_func)) 
snowball_tokens = data['tokens'].apply(lambda x: get_root(x, snowball_func)) 
wordnet_tokens = data['tokens'].apply(lambda x: get_root(x, wordnet_func)) 

```

</details>

```
WORD |           PORTER |         SNOWBALL |       LEMMATIZER |
      macklemore |        macklemor |        macklemor |       macklemore |
        shopping |             shop |             shop |         shopping |
            this |              thi |             this |             this |
         awesome |           awesom |           awesom |          awesome |
       mezzanine |         mezzanin |         mezzanin |        mezzanine |
          washed |             wash |             wash |           washed |
            this |              thi |             this |             this |
             his |               hi |              his |              his |
     handmedowns |       handmedown |       handmedown |      handmedowns |
        addition |            addit |            addit |         addition |
           thats |             that |             that |            thats |
        ignorant |            ignor |            ignor |         ignorant |
gettingswindledandpimped | gettingswindledandpimp | gettingswindledandpimp | gettingswindledandpimped |
```



### Visualizations


Type             |  Visual
:-------------------------:|:-------------------------:
10 Most Common Words Across Corpus |  ![](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/10commonpre.png)
Baseline Word Cloud |  ![](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/first_cloud.png)
Custom Processed Word Cloud |  ![](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/remove_expl_cloud.png)
2019 Processed Word Cloud |  ![](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/2019cloud.png)



## Topic Modeling

### Latent Dirichlet Allocation

***What is LDA?***

[Intuitive Guide to Latent Dirichlet Allocation](https://towardsdatascience.com/light-on-math-machine-learning-intuitive-guide-to-latent-dirichlet-allocation-437c81220158)

</br>

Topic modelling refers to the task of identifying topics that best describes a set of documents. These topics will only emerge during the topic modelling process (therefore called latent). And one popular topic modelling technique is known as Latent Dirichlet Allocation (LDA). Though the name is a mouthful, the concept behind this is very simple.

</br>

To tell briefly, LDA imagines a fixed set of topics. Each topic represents a set of words. And the goal of LDA is to map all the documents to the topics in a way, such that the words in each document are mostly captured by those imaginary topics.

<img align='center' src='https://miro.medium.com/max/1400/1*QQTk2TGyzhakGh0lZ9P03w.jpeg' />


#### Baseline LDA:

```
Topics found via LDA:

Topic #0:
expletive_0 love uh expletive_1 woo expletive_6 baby man money expletive_3 skrrt drop thun cardi bad

Topic #1:
expletive_3 expletive_1 expletive_0 expletive_4 baby love right cause time say god real tell want better

Topic #2:
gang gucci watch lil wicked drake cut love west kanye bust expletive_3 bop expletive_1 young
```
<details>
  <summary>
    More Topics
  </summary>

```
Topic #3:
hitta hittas love lil 2016 money black expletive_3 young ring saying rake world rich mask

Topic #4:
expletive_0 expletive_1 walk expletive_3 want love nothin talk money bout feel ball bank taste young

Topic #5:
expletive_0 expletive_3 expletive_4 hol really expletive_1 look want man em say cause money keys feel

Topic #6:
expletive_0 expletive_1 expletive_3 baby want expletive_4 hit love pop right expletive_2 ta girl cause money
```

</details>

#### Final LDA:

```
Topics found via LDA:

Topic #0:
walk talk gotta lot times want twerk dance bandz love break lil tell cabello moves good time man hit came

Topic #1:
feel thun drop stoner time type wanna want love tell good plug say wait man cause look girl hate face

Topic #2:
gang watch gucci cut cardi whip hot bop nae brr wrist kitchen 21 stir cartier fry huh chain woo nah
```
<details>
  <summary>
    More Topics
  </summary>

```
Topic #3:
dog maybe jesus beat say ride huh tried tryna want wanna leave cause baby skrrt time feed run gotta came

Topic #4:
hitta hittas look love wicked drake kanye west want panda future tap butt lil hours remix good dj dm girl

Topic #5:
baby girl right say better cause think tell want wanna turn crazy gave tryna man hit time looking come friends

Topic #6:
keys love feet woo lil different mask coco come clout big brown chase good savage talk ye bad time aap

Topic #7:
wanna bust taste goin time right real want mediocre better really timber cause rake big end tell love round come

Topic #8:
gas pedal tiimmy want new swear walkin man uh life right type em soul kill bet everybody knows git hit

Topic #9:
nothin money hit really bout jumpman quan worried bank lil big say woo cause new em low rap somethin boy

Topic #10:
want pop uh problem stop love bad right say em feelin look money tryna mind rollie good red young girl
```

</details>



#### LDA Visualizations:

[PRE LDA](https://boogiedev.github.io/HITMAKA-3000/lda.html)             |  [FINAL LDA](https://boogiedev.github.io/HITMAKA-3000/post_lda.html)
:-------------------------:|:-------------------------:
![](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/pre_lda.gif)  |  ![](https://github.com/boogiedev/HITMAKA-3000/blob/master/media/final_lda.gif)




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

### RAP Generation via RNN

```python
%tensorflow_version 1.x

from google.colab import files
from textgenrnn import textgenrnn
from datetime import datetime
import os

textgen.train_from_file('kodak_lyrics.txt', num_epochs=20)
```

#### Epoch 1
```
Epoch 1/20
5008/5008 [==============================] - 64s 13ms/step - loss: 1.3509
####################
Temperature: 0.2
####################
i dont want no more but i aint got no more baby

i got this **** in the street (yeah)

i was still a lil ****** when i got the streets

####################
```

#### Epoch 20 @ Different Temperature Hyperparameters
```
Epoch 20/20
5008/5008 [==============================] - 61s 12ms/step - loss: 0.9543
```
---

<p>
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/temp1.PNG">
  </img>
  
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/temp2.PNG">
  </img>
  
  <img src="https://raw.githubusercontent.com/boogiedev/HITMAKA-3000/master/media/temp3.PNG">
  </img>
</p>

---


### Performance and Manual Sentiment Analysis

Sample Output BARs| Thoughts
:--: | :--: |
im so fed up i dont even chase the same | Aligns with message, sounds like him
i fell in love with the pole, i be rollin in the open | Sounds like he is in a club
i be so drive it in my feet, i just wanna ride candy | ...?


---

<p>
  
  <img width="25%" align="right" src="https://static1.squarespace.com/static/551d9102e4b0cd11d25c2f4c/56788d7e05f8e228a3967706/5c0882766d2a733381843f5d/1544061951190/homepage_list-7.gif"></img>
  
</p>

***We had to stop because the KODAKBOT started becoming self aware, so we ceased to push this endeavour in order to protect humanity (and the rap scene).*** 

***HE'S TOO EVOLVED, 
HIS MOVEMENTS ARE TOO FAST, 
HIS LYRICALITY IS INSANE***

<br/>

## Future Considerations

- Flexmeter (Branding Finder)
- AD LIB Recognizer
- KODAKBOT E V O L V E D

## License
[MIT ©](https://choosealicense.com/licenses/mit/)

