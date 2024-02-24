from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..abfunc.stt import stt
from ..abfunc.ttsMal import tts_mal
from ..abfunc.ttsoai import tts_en
from .yt import bot

class Audio_bot_req(BaseModel):
    url : str
    audio_file : UploadFile
    lang : str

router = APIRouter()

@router.post('/audio_bot', tags = ["audio_bot"])
async def audio_bot(audio_bot_req : Audio_bot_req):
    if(audio_bot_req.lang=="en"):
        query = transcript(audio_bot_req.audio_file)
        reply = bot(url = audio_bot_req.url, is_query = True, query = query)
        tts_en(reply, "ttsen.mp3")
        with open("ttsen.mp3", "rb") as file:
            audio_data = file.read()
        return StreamingResponse(audio_data, media_type="audio/mpeg")
    elif(audio_bot_req.lang=="ml"):
        query = transcript(audio_bot_req.audio_file)
        reply = bot(url = audio_bot_req.url, is_query = True, query = query)
        tts_mal(reply,"ttsmal.mp3")
        with open("ttsmal.mp3", "rb") as file:
            audio_data = file.read()
        return StreamingResponse(audio_data, media_type="audio/mpeg")
    else:
        return "Language not available"