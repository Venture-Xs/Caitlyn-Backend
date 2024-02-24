import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi


yid = str(input("Enter YouTube video ID: "))
def bot(yid, is_query = False , query="") :
    # Get transcript of YouTube video
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
    else :
        message = {
            "role": "user",
            "content": f"Must return an array of JSON objects of the form: {{'summary_of_section': 'summary', 'time_stamp': '...'}} The article is as follows: {transcript}"
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
        return reply
    except Exception as e:
        print("Error communicating with OpenAI:", e)
        return 0

reply = bot(yid,True,"What is goggins talking about?")
print(reply)