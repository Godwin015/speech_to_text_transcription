from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import speech
from google.oauth2 import service_account
import os
import json

app = FastAPI()

# CORS settings (adjust origins as needed)
origins = [
    "https://godwin015.github.io",
    "https://speech-to-text-transcription.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Speech-to-text transcription backend is running!"}

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), language: str = "en-US"):
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid audio file type")

    audio_bytes = await audio.read()

    try:
        # Parse JSON string from environment variable
        creds_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        client = speech.SpeechClient(credentials=credentials)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code=language
        )

        audio_data = speech.RecognitionAudio(content=audio_bytes)

        response = client.recognize(config=config, audio=audio_data)

        if not response.results:
            return {"transcription": "No speech detected", "confidence": 0.0}

        result = response.results[0].alternatives[0]
        return {
            "transcription": result.transcript,
            "confidence": result.confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
