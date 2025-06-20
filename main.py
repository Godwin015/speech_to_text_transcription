from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio
import os

app = FastAPI()

# ✅ Enable CORS (update frontend domain in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://godwin015.github.io",  # your GitHub Pages frontend
        "https://speech-to-text-transcription.onrender.com"  # your Render backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Tell the Google SDK where the credentials are mounted
# This path must match the path you used in Render's Secret Files
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud-credentials.json"

@app.get("/")
async def root():
    return {"message": "Speech-to-text transcription backend is running!"}

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), language: str = "en-US"):
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid audio file type")

    try:
        audio_bytes = await audio.read()
        print("Audio Content Type:", audio.content_type)
        print("Audio Size:", len(audio_bytes))

        client = speech.SpeechClient()

        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code=language
        )

        audio_data = RecognitionAudio(content=audio_bytes)

        response = client.recognize(config=config, audio=audio_data)

        if not response.results:
            return {"transcription": "No speech detected", "confidence": 0.0}

        result = response.results[0].alternatives[0]
        return {
            "transcription": result.transcript,
            "confidence": result.confidence
        }

    except Exception as e:
        print("Error during transcription:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
