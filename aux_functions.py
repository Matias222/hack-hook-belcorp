from openai import OpenAI
from dotenv import load_dotenv

import requests
import os
import logging

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def handler_media(mensaje,request):
    
    if 'MediaContentType0' in request:
    
        media_type:str = request['MediaContentType0']

        if media_type.startswith('audio/'):
        
            mensaje = transcribe_audio(request["MediaUrl0"])

        else:

            mensaje= "-1"

    return mensaje


def transcribe_audio(media_url: str):

    audio = requests.get(media_url).content 

    with open("audio.wav", "wb") as audio_file:
        audio_file.write(audio)

    with open("audio.wav", 'rb') as audio_file:
        transcription = openai_client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="es")
    
    logging.info(f"WHISPER V2: {transcription.text}")
    
    return transcription.text