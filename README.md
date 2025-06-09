# FastAPI Audio Transcription Backend

This is a backend server built with **FastAPI** to handle audio file uploads and return transcription.

## Features

- Accepts audio file uploads
- Returns dummy transcription and confidence
- Ready for real integration (Google API, Whisper, etc.)
- CORS enabled for GitHub Pages frontend
- Deployable to [Render](https://render.com)

## How to Run Locally

```bash
# 1. Clone this repo
git clone https://github.com/your-username/fastapi-transcriber.git
cd fastapi-transcriber

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
uvicorn main:app --reload
