from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so your frontend on GitHub Pages can talk to this backend
origins = [
   # "http://localhost:3000",  # your local frontend testing address (optional)
    "https://godwin015.github.io/speech_to_text_transcription/",  # replace with your actual GitHub Pages URL
    "*",  # for testing you can allow all origins, but in production limit this!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), language: str = "en"):
    # Check file type (optional)
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid audio file type")
    
    # Save uploaded file locally (just for demo)
    contents = await audio.read()
    filename = f"temp_{audio.filename}"
    with open(filename, "wb") as f:
        f.write(contents)
    
    # Here you will call your transcription logic (Google API, Whisper, etc)
    # For now, return dummy response
    transcription = f"Transcription for file {audio.filename} in language {language}"
    confidence = 0.99  # Dummy confidence

    # Remove temp file if you want (optional)
    import os
    os.remove(filename)
    
    return {
        "transcription": transcription,
        "confidence": confidence
    }
