# 🎙️ VocalMate – Voice-Enabled Task Manager

> A multimodal productivity app that captures tasks via live speech or audio uploads, and syncs seamlessly with Google Calendar for real-time scheduling.

---

## 🚀 Features

- 🎤 **Voice Capture**: Add tasks using live speech or upload audio files.  
- 📝 **Speech-to-Text Pipeline**: Uses robust transcription models for accurate task capture.  
- 📅 **Calendar Integration**: Syncs tasks automatically with **Google Calendar API**.  
- ⚡ **Real-Time Scheduling**: Updates reflect instantly across your calendar.  
- 📊 **Dashboard View**: Visualize and manage tasks interactively.  

---

## 🛠 Tech Stack

- **Frontend/UI**: Streamlit  
- **Backend**: Python  
- **APIs**: Google Calendar API  
- **Libraries**: SpeechRecognition, PyDub, NumPy, Pandas  

---

## 📦 Setup & Installation

```bash
git clone https://github.com/bindujamalempati/VocalMate.git
cd VocalMate
pip install -r requirements.txt
Create a .env file with:

ini
Copy code
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret
GOOGLE_CALENDAR_API_KEY=your_key
🎯 Usage
Run locally:

bash
Copy code
streamlit run app.py
Speak directly into your mic or upload .wav/.mp3 files.

Confirm transcription → task added to Google Calendar.

📊 Example
Input (Speech)	Transcribed Text	Action
“Meeting with John at 5 PM”	Meeting with John at 5 PM	Added to Calendar ✅

📄 License
MIT License.
