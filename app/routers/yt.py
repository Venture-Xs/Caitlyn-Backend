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
        tx = YouTubeTranscriptApi.get_transcript(video_id=str(yid), languages=[
    "af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn",
    "eu", "be", "bho", "bs", "bg", "my", "ca", "ceb", "zh-Hans", "zh-Hant",
    "co", "hr", "cs", "da", "dv", "nl", "en", "eo", "et", "ee",
    "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", "gn", "gu",
    "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id",
    "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "kri",
    "ku", "ky", "lo", "la", "lv", "ln", "lt", "lb", "mk", "mg",
    "ms", "ml", "mt", "mi", "mr", "mn", "ne", "nso", "no", "ny",
    "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", "ro", "ru",
    "sm", "sa", "gd", "sr", "sn", "sd", "si", "sk", "sl", "so",
    "st", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th",
    "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy",
    "fy", "xh", "yi", "yo", "zu"
])
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
            "content": f"Must return a reply of size 50 to 80 words : The article is as follows: {transcript} the query about the article is :{str(query)}"
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
        if not is_query:
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