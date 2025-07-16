let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const fileInput = document.getElementById("fileInput");
const transcript = document.getElementById("transcript");
const spinner = document.getElementById("spinner");
const languageSelector = document.getElementById("language");
const darkToggle = document.getElementById("darkToggle");
const audioPlayer = document.getElementById("audioPlayer");
const downloadBtn = document.getElementById("downloadBtn");

// Set your backend URL
const BACKEND_URL = "https://huggingface.co/spaces/Gaadwhin/speech_to_text_api/transcribe";

// Initialize WaveSurfer
const waveform = WaveSurfer.create({
  container: "#waveform",
  waveColor: "lightblue",
  progressColor: "blue",
  height: 100
});

// Toggle Dark Mode
darkToggle.addEventListener("change", () => {
  document.body.classList.toggle("dark");
  document.querySelector(".container").classList.toggle("dark");
});

// Start recording
recordBtn.onclick = async () => {
  waveform.empty();
  audioPlayer.classList.add("hidden");
  downloadBtn.classList.add("hidden");

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = event => {
    audioChunks.push(event.data);
  };

  mediaRecorder.onstop = () => {
    const blob = new Blob(audioChunks, { type: "audio/webm" });
    const audioURL = URL.createObjectURL(blob);

    waveform.load(audioURL);
    audioPlayer.src = audioURL;
    audioPlayer.classList.remove("hidden");

    sendAudioToBackend(blob);
  };

  mediaRecorder.start();
  recordBtn.disabled = true;
  stopBtn.disabled = false;
};

// Stop recording
stopBtn.onclick = () => {
  mediaRecorder.stop();
  recordBtn.disabled = false;
  stopBtn.disabled = true;
};

// Upload audio file
fileInput.onchange = () => {
  const file = fileInput.files[0];
  if (!file) return;

  // Optional: Validate audio type
  if (!file.type.startsWith("audio/")) {
    alert("Please upload a valid audio file.");
    return;
  }

  const audioURL = URL.createObjectURL(file);
  waveform.load(audioURL);
  audioPlayer.src = audioURL;
  audioPlayer.classList.remove("hidden");
  downloadBtn.classList.add("hidden");

  sendAudioToBackend(file);
};

// Send audio to backend for transcription
async function sendAudioToBackend(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob);
  formData.append("language", languageSelector.value);

  transcript.textContent = "Transcribing...";
  transcript.classList.remove("visible");
  spinner.classList.remove("hidden");

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const result = await response.json();
    console.log("Backend response:", result);

    transcript.textContent = result.transcription || "No transcription found.";
    transcript.classList.remove("visible");

    setTimeout(() => {
      transcript.classList.add("visible");
    }, 100);

    if (result.transcription) {
      downloadBtn.classList.remove("hidden");
      setupDownload(result.transcription);
    }
  } catch (error) {
    console.error("Transcription error:", error);
    transcript.textContent = "Error during transcription.";
  } finally {
    spinner.classList.add("hidden");
  }
}

// Download .txt
function setupDownload(text) {
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  downloadBtn.href = url;
  downloadBtn.download = "transcription.txt";
}
