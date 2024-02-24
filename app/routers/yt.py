import os
import json
from pytube import YouTube
from openai import OpenAI
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

def bot(url, is_query = False , query = "", generateTest = False) :
    # Get transcript of YouTube video
    is_query = bool(is_query)
    generateTest = bool(generateTest)
    yt_obj = YouTube(url)
    yid = yt_obj.video_id
    try:
        tx = YouTubeTranscriptApi.get_transcript(video_id=str(yid), languages=['en', 'ru', 'ml'])
        transcript = ""
        for i in tx:
            transcript += i['text']
    except Exception as e:
        print("Error retrieving transcript:", e)
        exit()

    # Initialize OpenAI client
    load_dotenv()
    client = OpenAI(
        api_key= os.getenv("API_KEY"),
    )


    messages = []
    if is_query :
        message = {
            "role": "user",
            "content": f"Must return an array of JSON objects of the form: {{'reply': 'reply'}} The article is as follows: {transcript} the query about the article is :{str(query)}"
        }
    elif generateTest:
        message = {
            "role": "user",
            "content": f'Must return an array of JSON objects of the form: {{"questions": [{{"q1":"...","o1":"...",o2:"...","o3":"...","o4":"...","answer":"..."}},{{"q2":"...","o1":"...",o2:"...","o3":"...",o4:"...","answer":"..."}},...]}} The article is as follows: {transcript} generate a mcq test with 5 questions from this article'
        } 
    else :
        message = {
            "role": "user",
            "content": f'Must return an array of JSON objects of the form: {{"title_of_section":"title",summary_of_section": "summary", "time_stamp": "..."}} The article is as follows: {transcript}.Must provide time_stamp at all cost'
        }
    messages.append(message)
    try:
        chat_completion = client.chat.completions.create(
            messages= messages,
            model="gpt-3.5-turbo",
        )

        reply = chat_completion.choices[0].message.content
        reply.replace("\'","\"")
        reply.replace("json","")
        reply = json.loads(reply)
        print(reply)
        return reply
    except Exception as e:
        print("Error communicating with OpenAI:", e)
        return 0
    
'''    
def print_reply():  
    reply = bot("https://www.youtube.com/watch?v=9goOuIy8Ok4")
    print(reply)
print_reply()
'''