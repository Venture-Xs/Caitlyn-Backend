import pytube as pt
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

def yt_to_mp3(link):
    yt = pt.YouTube(link)
    stream = yt.streams.filter(only_audio=True)[0]
    stream.download(filename="audio_english.mp3")
    audio = "audio_english.mp3"
    audio_file= open(audio, "rb")
    return audio_file
    
def transcribe(audio_file):
    transcript = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file,
      response_format="text",
      stream=True,
    )
    return transcript

def stt(url):
    audio =  yt_to_mp3(url)
    transcript =  transcribe(audio)
    return transcript
   


