# VocalMate – AI Task Assistant

> Your intelligent voice+text assistant for smart task management, scheduling, and calendar integration.

---

## 🌟 Overview

VocalMate is a voice-enabled task manager powered by GPT that helps users:

* ✍️ Add tasks via voice or text
* 🔍 Parse vague instructions (e.g., "meeting next Wed 3pm")
* 🔔 Generate smart daily digests
* 🌐 Transcribe uploaded audio meetings (e.g., .mp3)
* 🗓️ Sync select tasks with Google Calendar

---

## 🔧 Features

| Feature                       | Description                                                         |
| ----------------------------- | ------------------------------------------------------------------- |
| 🌐 Voice Input + Audio Upload | Accepts direct voice or .mp3/.wav file uploads                      |
| 🤖 GPT Task Parsing           | Converts natural language into structured task objects              |
| ⚖️ Auto Categorization        | Classifies tasks as `Work`, `Personal`, etc.                        |
| ⏰ Smart Digest                | Summarizes the user's day with categorized task insights            |
| 🗓️ Calendar Sync             | Optionally syncs user-approved tasks with Google Calendar via OAuth |
| 📁 Offline Storage            | Stores tasks locally in JSON or SQLite                              |



---

## 📚 Tech Stack

| Purpose            | Tools / Libraries                   |
| ------------------ | ----------------------------------- |
| UI                 | Streamlit                           |
| NLP + Task Parsing | OpenAI GPT (or Claude)              |
| Audio Input        | `speech_recognition`, `pydub`       |
| Audio File Support | `.mp3`, `.wav`, via `tempfile`      |
| Calendar API       | Google Calendar API + `google-auth` |
| Task Storage       | JSON or SQLite                      |

---

## ♻️ Setup Instructions

```bash
# 1. Clone this repo
$ git clone https://github.com/your-username/vocalmate
$ cd vocalmate

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Add your OpenAI + Google API credentials
- Place `credentials.json` (Google OAuth) in root
- Set your `OPENAI_API_KEY` in a `.env` file or environment

# 4. Run locally
$ streamlit run app.py
```

---

## 🎥 Demo Video

---

## 🌐 Live App (Optional)

Deploy your app on [Streamlit Cloud](https://streamlit.io/cloud), [Render](https://render.com), or [Hugging Face Spaces](https://huggingface.co/spaces)

---

## ✨ Future Improvements

* Integrate proactive reminders with alerts
* Auto-detect recurring tasks and conflicts
* Slack/Discord bot version
* Public transcription and summarization API

---

## 🙏 Acknowledgments

Built with OpenAI, Google Cloud, and lots of late-night debugging.

---

## 📄 License

MIT License. Feel free to fork and improve!
