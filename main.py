from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio
import os
import json

app = FastAPI()

# Enable CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Step 1: Create credential file dynamically from env var
@app.on_event("startup")
async def load_gcloud_credentials():
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not creds_json:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set")
    with open("gcloud-credentials.json", "w") as f:
        f.write(creds_json)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-credentials.json"

# ✅ Step 2: Transcription Endpoint
@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        print("Audio Content Type:", audio.content_type)
        print("Audio Size:", len(audio_bytes))

        client = speech.SpeechClient()

        audio_config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US"
        )

        audio_data = RecognitionAudio(content=audio_bytes)

        response = client.recognize(config=audio_config, audio=audio_data)

        # Extract transcription
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
        else:
            transcript = "No transcription found"

        return {"transcript": transcript}

    except Exception as e:
        print("Error during transcription:", e)
        return {"error": str(e)}
