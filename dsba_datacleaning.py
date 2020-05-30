# -*- coding: utf-8 -*-
"""DSBA_DataCleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wQBVfHifbOK5v_bjbloTKGIE1s5mJMWG
"""

# Fetching Hit songs from Billboard by specifiying the year and appending it to billboard_songDataset list
  # chart-type = hot-100
  # chart-date = From which year we are retreiving the hit songs.

pip install billboard.py

import billboard
import pandas as pd
from datetime import datetime

billboard_songDataset = []
billboard_chart = []
chart_type = 'hot-100'
chart_date = ['1990-01-01','1991-01-01','1992-01-01','1993-01-01','1998-01-01','1999-01-01','2000-01-01','2005-01-01','2006-01-01','2007-01-01','2008-01-01','2013-01-01','2014-01-01','2015-01-01','2016-01-01','2017-01-01','2018-01-01','2019-01-01','2020-01-01']
#chart_date = ['1990-01-01','1991-01-01','1992-01-01','1993-01-01','1994-01-01','1995-01-01','1996-01-01','1997-01-01','1998-01-01','1999-01-01','2000-01-01','2001-01-01','2002-01-01','2003-01-01','2004-01-01','2005-01-01','2006-01-01','2007-01-01','2008-01-01','2009-01-01','2010-01-01','2011-01-01','2012-01-01','2013-01-01','2014-01-01','2015-01-01','2016-01-01','2017-01-01','2018-01-01','2019-01-01','2020-01-01']
len_chartDate = len(chart_date)

for year in range(0,len_chartDate):
  print(chart_date[year])
  data = billboard.ChartData(chart_type,chart_date[year])
  for elem in data:
    billboard_songDataset.append([elem.title, elem.artist])

#print(len(billboard_songDataset))

##Converting the list to pandas dataFrame and labelling songs as Hit with additional column BillBoard_Hit, '1' showing Hit and '0' Flop

billboard_songDataset = pd.DataFrame(billboard_songDataset)
billboard_songDataset.columns = ['Song_Title','Song_Artist']
billboard_songDataset['BillBoard_Hit'] = 1
billboard_songDataset.head()

## Intializing the spotify feature for updating values in future

billboard_songDataset[ "spotify_danceability"] = 0
billboard_songDataset["spotify_energy"] = 0
billboard_songDataset["lspotify_oudness"] = 0
billboard_songDataset["spotify_speechiness"] = 0
billboard_songDataset["spotify_acousticness"] = 0
billboard_songDataset["spotify_instrumentalness"] = 0
billboard_songDataset["spotify_liveness"] = 0
billboard_songDataset["spotify_valence"] = 0
billboard_songDataset["spotify_tempo"] = 0
billboard_songDataset["spotify_duration_ms"] = 0
billboard_songDataset["spotify_danceability"] = 0

pip install spotipy

pip install requests

## Spotify authorization and session manager
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'f1b4ea97e7db4bf1b7e1348cbcb97f7c'
client_secret = '2c98c2d53ea647ea84e730cbd41f35cd'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

## Function to map API data to respective row in dataframe/dataset

def spotify_songFeatures_mapper(songName,spotify_songFeatures):
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_danceability']] = spotify_songFeatures["danceability"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_energy']] = spotify_songFeatures["energy"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['lspotify_oudness']] = spotify_songFeatures["loudness"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_speechiness']] = spotify_songFeatures["speechiness"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_acousticness']] = spotify_songFeatures["acousticness"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_instrumentalness']] = spotify_songFeatures["instrumentalness"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_liveness']] = spotify_songFeatures["liveness"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_valence']] = spotify_songFeatures["valence"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_tempo']] = spotify_songFeatures["tempo"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_duration_ms']] = spotify_songFeatures["duration_ms"]
  billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName,['spotify_danceability']] = spotify_songFeatures["danceability"]

## Feaching Song Features from Spotify API and Using mapper function updating the values.

songList = billboard_songDataset["Song_Title"][0:20]

for song in songList:
  spotify_response = sp.search(q = "name:" + song )
  if spotify_response["tracks"]["items"]:
    spotify_songID = spotify_response["tracks"]["items"][0]["id"]
    spotify_songFeatures = sp.audio_features(spotify_songID)[0]
    spotify_songFeatures_mapper(song, spotify_songFeatures)

"""**TWITTER DATA RETRIEVAL**"""

## Twitter Token values (** I have created an APP in twitter devloper account for DSBA **)

Twitter_CONSUMER_KEY = "T94aK9PaTzpWoIjXe0183v9CS"
Twitter_CONSUMER_SECRET = "jcAu3IZN5zg87hIeBn4Y8qVduVuYpuFcGt1Q8Zl3eW0DFf1FFq"
Twitter_ACCESS_TOKEN = "1245416768732086278-TkeSL69lQQ3duYP6TWuIhsn7bxpZHf"
Twitter_ACCESS_SECRET = "NTmonA7kMTIZhHYglLA4xYcJxcKezZVg7Otity8plR3LU"

pip install python-twitter

## Creating twitter session with token

import twitter
t = twitter.Api(consumer_key=Twitter_CONSUMER_KEY,
                consumer_secret=Twitter_CONSUMER_SECRET,
                access_token_key=Twitter_ACCESS_TOKEN,
                access_token_secret=Twitter_ACCESS_SECRET)

## Intilaizing twitter column, to append tweets in future

billboard_songDataset["Tweets"] = 0

## Removing " ' " from song Name
## As if we are searching tweets with songName as hashtag and it has " ' " in its name, twitter is throwing authorization error

songList_twitter = []
songList = billboard_songDataset["Song_Title"][0:20]
for song in songList:
  if "'" in song:b
    song = song.replace("'", "")
  songList_twitter.append(song)
print(songList_twitter)

## Funtion to update tweets of song in dataFrame/dataset
def tweetMapper(songName,song_tweets):
    billboard_songDataset.loc[ billboard_songDataset['Song_Title'] == songName, ['Tweets']] = song_tweets

## Retrieving tweets with hashtag of songName
for songName in songList_twitter:
  song_tweets = []
  q= 'q=%23'+songName
  print(q)
  twitter_tweets = t.GetSearch(raw_query=str(q))
  for tweet in twitter_tweets:
    song_tweets.append(tweet.text)
  #print(str(song_tweets))
  tweetMapper(songName,str(song_tweets))

## Final output 
billboard_songDataset[0:20]