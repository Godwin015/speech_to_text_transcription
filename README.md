# 🗣️ Speech-to-Text Transcription App

This is a full-stack speech-to-text transcription tool built with:

- 🔧 **FastAPI** (Python backend)
- 🧠 **OpenAI Whisper** (runs locally, no API key needed)
- 🎙️ **MediaRecorder API** + Vanilla JS frontend
- 📦 **Deployed on Render (backend)** & **GitHub Pages (frontend)**


## 🚀 Live Demo

- 🌐 Frontend: [https://godwin015.github.io](https://godwin015.github.io)
- ⚙️ Backend: [https://speech-to-text-transcription.onrender.com](https://speech-to-text-transcription.onrender.com)


## 📂 Project Structure

├── main.py # FastAPI backend with Whisper
├── requirements.txt # Python dependencies
├── render.yaml # Render deployment config
├── index.html # Frontend HTML (GitHub Pages)
├── script.js # JavaScript (audio recording, sending, etc.)
├── styles.css # Custom CSS with dark mode
└── README.md # Project documentation



## 🎯 Features

- 🎤 Record audio directly in the browser
- 📁 Upload audio files (`.webm`, `.mp3`, etc.)
- 🌍 Language selection (English, Spanish, French, etc.)
- 💬 Live transcription using OpenAI Whisper
- 💡 Dark mode toggle
- ⬇️ Download transcribed text


## 🧠 How It Works

1. Frontend records audio using `MediaRecorder`.
2. Audio is sent to a FastAPI backend (`/api/transcribe`).
3. The backend uses `whisper` to transcribe speech into text.
4. The result is returned and displayed on the page.
5. User can download transcription as `.txt`.


## 📦 Installation (for local testing)

### Backend

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
uvicorn main:app --reload

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: https://ffmpeg.org/download.html

Frontend
Open index.html directly in your browser
Or host it with GitHub Pages.

⚙️ Deployment
On Render (Backend)
Render uses render.yaml to:
Install ffmpeg
Install Python packages
Run FastAPI with uvicorn
Push changes to GitHub or trigger manual deploy.

🧪 Tech Stack
FastAPI – Python web framework
OpenAI Whisper – Local speech-to-text transcription
FFmpeg – Audio format handling
Vanilla JS – Recording + file handling
WaveSurfer.js – Audio waveform visualization
Render – Backend deployment
GitHub Pages – Frontend hosting

🙋🏽‍♂️ Author
Godwin Edward
Cybersecurity & AI Student
GitHub @godwin015
LinkedIn https://www.linkedin.com/in/godwin-edward-25961825a/
