from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..abfunc.stt import stt
from ..abfunc.stt import transcribe
from ..abfunc.ttsMal import tts_mal
from ..abfunc.ttsoai import tts_en
from .yt import bot
import os,shutil
from pydub import AudioSegment

class Audio_bot_req(BaseModel):
    url : str
    audio_file : UploadFile
    lang : str

router = APIRouter()
upload_dir ='./'
@router.post('/audio_bot', tags = ["audio_bot"])
async def audio_bot(url: str, audio_file: UploadFile, lang: str):
    # Save the uploaded file locally
    file_path = os.path.join(upload_dir, audio_file.filename)
    with open(file_path, "wb") as file:
        shutil.copyfileobj(audio_file.file, file)

    # Convert the audio file to MP3 format
    mp3_file_path = os.path.join(upload_dir, f"{audio_file.filename.split('.')[0]}.mp3")
    audio_segment = AudioSegment.from_file(file_path)
    audio_segment.export(mp3_file_path, format="mp3")
    audio= open(mp3_file_path, "rb")
    query = transcribe(audio)
    print(query)
    reply = bot(url = url, is_query = True, query = query)
    print(reply)
    if(lang=="en"):
        speech_file_path = tts_en(reply, "ttsen.mp3")
        audio_segment = AudioSegment.from_file(speech_file_path)
        mp3_bytes = audio_segment.export(format="mp3").read()
        
        # Return the MP3 audio as part of the JSON response
        return {"audio_file": mp3_bytes.decode("latin-1")}
    elif(lang=="ml"):
        speech_file_path = tts_mal(reply,"ttsmal.mp3")
        # Convert the audio file to MP3 format
        audio_segment = AudioSegment.from_file(speech_file_path)
        mp3_bytes = audio_segment.export(format="mp3").read()

        # Return the MP3 audio as part of the JSON response
        return {"audio_file": mp3_bytes.decode("latin-1")}
    else:
        return "Language not available"