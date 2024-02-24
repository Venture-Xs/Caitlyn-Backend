import requests
import base64
import io
from pydub import AudioSegment

def tts_mal(prompt,outputPath):
    # Define new data to create
    new_data = {
        "controlConfig": {
            "dataTracking": "true"
        },
        "input": [
            {
                "source": prompt
            }
        ],
        "config": {
            "gender": "female",
            "language": {
                "sourceLanguage": "ml"
            }
        }
    }

    # The API endpoint to communicate with
    url_post = "https://demo-api.models.ai4bharat.org/inference/tts"

    # A POST request to tthe API
    post_response = requests.post(url_post, json=new_data)

    # Print the response
    response_data = post_response.json()
    print(response_data)

    # Extract audio content from the response
    audio_content_base64 = response_data["audio"][0]["audioContent"]

    # Decode base64 and convert to AudioSegment
    audio_data = base64.b64decode(audio_content_base64)
    audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))

    # Save the AudioSegment as an MP3 file
    audio_segment.export(outputPath, format="mp3")


#tts_mal("ഇന്ത്യയിൽ കേരള സംസ്ഥാനത്തിലും ഭാഗികമായി കേന്ദ്രഭരണ പ്രദേശങ്ങളായ ലക്ഷദ്വീപിലും പോണ്ടിച്ചേരിയുടെ ഭാഗമായ മാഹിയിലും തമിഴ്നാട്ടിലെ കന്യാകുമാരി ജില്ലയിലും നീലഗിരി ജില്ലയിലെ ഗൂഡല്ലൂർ താലൂക്കിലും സംസാരിക്കപ്പെടുന്ന ഭാഷയാണ് മലയാളം","ttsmal.mp3")