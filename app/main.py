from fastapi import FastAPI

from .routers import chat_bot, audio_bot

app = FastAPI()

app.include_router(chat_bot.router)
app.include_router(audio_bot.router)

@app.get('/')
async def root():
    return "hello"