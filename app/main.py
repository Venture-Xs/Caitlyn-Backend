from fastapi import FastAPI
import uvicorn
import os
from .routers import chat_bot, audio_bot

app = FastAPI()

app.include_router(chat_bot.router)
app.include_router(audio_bot.router)

@app.get('/')
async def root():
    return "hello"

if __name__ == "__main__":
    port = os.getenv("PORT")
    if not port:
        port = 8080
    uvicorn.run(app, host="0.0.0.0", port=8080) 
