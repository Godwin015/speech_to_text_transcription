# 🎤 Speech-to-Text Transcription Tool

A lightweight **speech-to-text web application** that converts spoken words into text using **OpenAI Whisper API**. The app supports **multiple languages**, has a **colorful and responsive UI**, and is hosted with a **GitHub frontend** and a **Hugging Face backend** for easy access.

---

## 🚀 Features

* **Real-time Speech Recognition** – Converts audio input into text seamlessly.
* **Multi-Language Support** – Transcribes speech in various languages accurately.
* **FastAPI Backend** – Handles transcription logic and API requests efficiently.
* **Responsive, Colorful UI** – Animated, user-friendly interface for smooth interaction.
* **Deployed Frontend & Backend** – Frontend hosted on **GitHub Pages**, backend on **Hugging Face Spaces**.

---

## 🛠 Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** FastAPI, Python, OpenAI Whisper
* **Deployment:** GitHub Pages (frontend), Hugging Face Spaces (backend)
* **Other Tools:** FFmpeg, Python-Multipart

---

## 🔗 Live Demo

**[Try the App Here](https://godwin015.github.io/speech_to_text_transcription/)**

---

## 📂 Project Structure

```
speech_to_text_transcription/
│
├── frontend/              # HTML, CSS, JS files
├── backend/               # FastAPI app, Whisper integration
├── requirements.txt       # Backend dependencies
├── Dockerfile             # For deployment
└── README.md              # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Godwin015/speech_to_text_transcription.git
cd speech_to_text_transcription
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend Locally

```bash
uvicorn app:app --reload
```

The API will run on `http://127.0.0.1:8000/`.

### 4. Open the Frontend

Simply open `index.html` in your browser or deploy using GitHub Pages.

---

## 💡 Future Improvements

* Add **user authentication** to save transcriptions.
* Support **file uploads (MP3/WAV)** for offline transcription.
* Integrate **real-time streaming** for live captions.
* Deploy on **Railway or Render** for faster backend performance.

---

## 🧑‍💻 Author

**Godwin Edward**

* Portfolio: [GitHub](https://github.com/Godwin015)
* LinkedIn: *(https://www.linkedin.com/in/godwin-edward-25961825a/)*
* Email: *(godwynedward015@gmail.com)*

---
