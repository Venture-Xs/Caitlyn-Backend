from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..abfunc.stt import stt
from ..abfunc.stt import transcribe
from ..abfunc.ttsMal import tts_mal
from ..abfunc.ttsoai import tts_en
from .yt import bot

class Audio_bot_req(BaseModel):
    url : str
    audio_file : UploadFile
    lang : str

router = APIRouter()

@router.post('/audio_bot', tags = ["audio_bot"])
async def audio_bot(url: str, audio_file: UploadFile, lang: str):
    query = transcribe(audio_file)
    reply = bot(url = url, is_query = True, query = query)
    if(lang=="en"):
        tts_en(reply, "ttsen.mp3")
        with open("ttsen.mp3", "rb") as file:
            audio_data = file.read()
        return StreamingResponse(audio_data, media_type="audio/mpeg")
    elif(lang=="ml"):
        tts_mal(reply,"ttsmal.mp3")
        with open("ttsmal.mp3", "rb") as file:
            audio_data = file.read()
        return StreamingResponse(audio_data, media_type="audio/mpeg")
    else:
        return "Language not available"