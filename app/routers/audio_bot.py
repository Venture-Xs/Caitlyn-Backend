from fastapi import APIRouter, UploadFile, File
from ..abfunc.stt import stt
from ..abfunc.ttsMal import tts_mal
from ..abfunc.ttsoai import tts_en
from yt import bot
class Audio_bot_req(BaseModel):
    url : str
    audio_file : UploadFile
    lang : str

router = APIRouter()

@router.post('/audio_bot', tags = ["audio_bot"])
async def audio_bot(audio_bot_req : Audio_bot_req):
    if(audio_bot_req.lang=="en"):
        query = transcript(audio_bot_req.audio_file)
        bot(url=audio_bot_req.url, )