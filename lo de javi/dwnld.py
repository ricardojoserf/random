import os, sys, deezer
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = config.DEVELOPER_KEY

def youtube_search(query):

  youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
  items = youtube.search().list(q=query, part="id,snippet", maxResults="5").execute().get("items", [])

  try:

    i = 0
    while(items[i]["id"]["kind"] != "youtube#video"):
      i = i + 1
    title = items[i]["snippet"]["title"]
    video_id = items[i]["id"]["videoId"]

    print "Downloading '"+title+"'"
    os.system("youtube-dl —extract-audio —audio-format mp3 —audio-quality 0 http://www.youtube.com/watch?v="+video_id + " > /dev/null 2>&1")
  
  except Exception as e:
    print str(e.message)


if name == "main":

  obj_id = sys.argv[1]
  song_search = []

  client = deezer.Client()
  song_list = client.get_playlist(obj_id).tracks

  for song in song_list:
    title = song.title
    artist = song.get_artist().name
    song_search.append((title + " " + artist).encode('utf8')) 
  
  for song_query in song_search:
    youtube_search(song_query)