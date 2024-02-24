from fastapi import APIRouter
from pydantic import BaseModel
from yt import bot

class Chat_bot_req(BaseModel):
    url : str
    isQuery: str #bool True/False
    query: str
    generateTest: str #bool

router = APIRouter()

@router.post('/chat_bot', tags = ["chat_bot"])
async def chat_bot(chat_bot_req : Chat_bot_req):
    reply = await bot(url= chat_bot_req.url, is_query= chat_bot_req.isQuery, query= chat_bot_req.query, generateTest= chat_bot_req.generateTest)
    return {"reply" : reply}