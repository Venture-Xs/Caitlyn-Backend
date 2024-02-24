from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
openai = OpenAI(api_key=os.getenv("API_KEY"))

def tts_en(prompt,outputPath):
    speech_file_path = Path(__file__).parent / outputPath
    response = openai.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=prompt
    )
    response.stream_to_file(speech_file_path)

#tts_en("Hey there I'm Madab","ttsen.mp3")