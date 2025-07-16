import whisper
import tempfile
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# ✅ Enable CORS for frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://godwin015.github.io",
        "https://speech-to-text-transcription.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Whisper model once (outside route for efficiency)
model = whisper.load_model("tiny")  # or use "tiny", "small", "medium", "large"

@app.get("/")
async def root():
    return {"message": "Whisper-based transcription backend is running!"}

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), language: str = "en"):
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid audio file type")

    try:
        # Save uploaded audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        # Transcribe using Whisper
        result = model.transcribe(tmp_path, language=language)

        # Clean up temp file
        os.remove(tmp_path)

        return {
            "transcription": result["text"],
            "language_detected": result.get("language", "unknown")
        }

    except Exception as e:
        print("Error during transcription:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
