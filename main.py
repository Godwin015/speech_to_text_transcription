from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import speech
import os

# Optional: Set this if not already done in your deployment environment
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account.json"

app = FastAPI()

# Allow CORS for your frontend URLs
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

    # 🔍 Debugging output
    print("Audio Content Type:", audio.content_type)
    print("Audio Size:", len(audio_bytes))  # in bytes

    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code=language
    )

    audio_data = speech.RecognitionAudio(content=audio_bytes)

    try:
        response = client.recognize(config=config, audio=audio_data)

        if not response.results:
            raise HTTPException(status_code=400, detail="No transcription found. Make sure the audio is clear and properly formatted.")

        result = response.results[0].alternatives[0]
        return {
            "transcription": result.transcript,
            "confidence": result.confidence
        }

    except Exception as e:
        print("Transcription Error:", str(e))  # Show error in logs
        raise HTTPException(status_code=500, detail="Transcription failed: " + str(e))
