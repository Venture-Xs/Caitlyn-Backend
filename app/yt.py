import pathlib
import textwrap
import openai
from youtube_transcript_api import YouTubeTranscriptApi


outls = []
yid = str(input("Enter youtube video id:"))
tx = YouTubeTranscriptApi.get_transcript(video_id = yid, languages = ['en','ru','ml'])

transcript = ""
for i in tx:
    transcript += i['text']

#print(transcript)
    

