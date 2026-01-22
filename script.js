let mediaRecorder;
let audioChunks = [];

// DOM Elements
const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const fileInput = document.getElementById("fileInput");
const transcript = document.getElementById("transcript");
const spinner = document.getElementById("spinner");
const languageSelector = document.getElementById("language");
const darkToggle = document.getElementById("darkToggle");
const audioPlayer = document.getElementById("audioPlayer");
const downloadBtn = document.getElementById("downloadBtn");
const copyBtn = document.getElementById("copyBtn");

const BACKEND_URL = "https://Gaadwhin-speech-to-text-api.hf.space/api/transcribe";

// Initialize WaveSurfer
const waveform = WaveSurfer.create({
  container: "#waveform",
  waveColor: "#cbd5e1",
  progressColor: "#6366f1",
  height: 80,
  barWidth: 2,
  borderRadius: 3,
  responsive: true
});

// Toggle Dark Mode
darkToggle.addEventListener("change", () => {
  document.body.classList.toggle("dark");
  const isDark = document.body.classList.contains("dark");
  waveform.setOptions({
    waveColor: isDark ? "#475569" : "#cbd5e1",
    progressColor: "#818cf8"
  });
});

// Copy to Clipboard
copyBtn.onclick = async () => {
  const text = transcript.textContent;
  try {
    await navigator.clipboard.writeText(text);
    const originalContent = copyBtn.innerHTML;
    copyBtn.innerHTML = `<i data-lucide="check"></i> Copied!`;
    lucide.createIcons();
    setTimeout(() => {
      copyBtn.innerHTML = originalContent;
      lucide.createIcons();
    }, 2000);
  } catch (err) {
    console.error("Failed to copy!", err);
  }
};

// Start recording
recordBtn.onclick = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    waveform.empty();
    audioPlayer.classList.add("hidden");
    downloadBtn.classList.add("hidden");
    copyBtn.classList.add("hidden");

    mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
    
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
    recordBtn.innerHTML = `<i data-lucide="mic-off"></i> Recording...`;
    recordBtn.classList.add("recording-pulse");
    lucide.createIcons();
  } catch (err) {
    alert("Microphone access is required to record audio.");
  }
};

stopBtn.onclick = () => {
  mediaRecorder.stop();
  recordBtn.disabled = false;
  stopBtn.disabled = true;
  recordBtn.innerHTML = `<i data-lucide="mic"></i> Start Recording`;
  recordBtn.classList.remove("recording-pulse");
  lucide.createIcons();
};

fileInput.onchange = () => {
  const file = fileInput.files[0];
  if (!file) return;

  const audioURL = URL.createObjectURL(file);
  waveform.load(audioURL);
  audioPlayer.src = audioURL;
  audioPlayer.classList.remove("hidden");
  sendAudioToBackend(file);
};

async function sendAudioToBackend(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob);
  formData.append("language", languageSelector.value);

  transcript.textContent = "Processing audio...";
  spinner.classList.remove("hidden");

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("Backend error");

    const result = await response.json();
    const text = result.transcription || "No text detected.";
    
    transcript.textContent = text;
    
    if (result.transcription) {
      downloadBtn.classList.remove("hidden");
      copyBtn.classList.remove("hidden");
      setupDownload(text);
    }
  } catch (error) {
    transcript.textContent = "Error: Could not reach the transcription server.";
    console.error(error);
  } finally {
    spinner.classList.add("hidden");
  }
}

function setupDownload(text) {
  const blob = new Blob([text], { type: "text/plain" });
  downloadBtn.href = URL.createObjectURL(blob);
  downloadBtn.download = "transcription.txt";
}
