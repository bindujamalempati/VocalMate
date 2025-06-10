import streamlit as st
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from agent import handle_command
from task_manager import view_tasks, delete_task
from calendar_sync import create_google_event

st.set_page_config(page_title="🎤 VocalMate – AI Task Assistant", layout="centered")
st.title("🎤 VocalMate – AI Task Assistant")

st.markdown("""
Welcome to **VocalMate**, your intelligent assistant for organizing tasks and syncing events to Google Calendar.  
Try entering a task like:  
- `team standup next Wednesday 9am`  
- or upload a voice file like `birthday dinner next Saturday at 8pm`
""")

# -------------------------------
# 📝 TEXT TASK INPUT
# -------------------------------
st.subheader("🧠 Type Your Task")
text_input = st.text_input("Enter your task", placeholder="e.g., project review next Monday at 10am")
if st.button("➕ Add Task"):
    if text_input.strip():
        result = handle_command(text_input)
        st.success(result)
    else:
        st.warning("Please enter a valid task.")

# -------------------------------
# 🔊 AUDIO FILE UPLOAD
# -------------------------------
st.subheader("🎧 Upload a Voice File (.mp3 or .wav)")
uploaded_audio = st.file_uploader("Upload your voice note", type=["mp3", "wav"])

from pydub import AudioSegment

if uploaded_audio:
    try:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_input:
            temp_input.write(uploaded_audio.read())
            temp_input_path = temp_input.name

        # Convert to WAV for better compatibility
        audio = AudioSegment.from_file(temp_input_path)
        temp_wav_path = temp_input_path.replace(".mp3", ".wav")
        audio.export(temp_wav_path, format="wav")

        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            st.success(f"🗣 Recognized: {text}")
            result = handle_command(text)
            st.write(result)

    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"❌ API error: {e}")
    except Exception as e:
        st.error(f"❌ File error: {e}")


# -------------------------------
# 📋 LIST ALL TASKS
# -------------------------------
st.markdown("---")
st.subheader("📋 Your Tasks")

tasks = view_tasks(return_as_list=True)
if tasks:
    for i, task in enumerate(tasks, 1):
        col1, col2, col3 = st.columns([5, 1, 2])
        with col1:
            st.markdown(f"**{i}. {task['description']}**  \n_Category_: {task['category']}  \n_Due_: {task['due_date']}")
        with col2:
            if st.button("🗑️", key=f"del_{i}"):
                delete_task(i - 1)
                st.rerun()
        with col3:
            if st.button("📆 Sync", key=f"sync_{i}"):
                link = create_google_event(task["description"], task["due_date"])
                if link:
                    st.success(f"[Event Synced]({link})")
                else:
                    st.error("❌ Failed to sync with Calendar.")
else:
    st.info("No tasks yet. Add one!")

# -------------------------------
# 📊 SMART DIGEST
# -------------------------------
st.markdown("---")
st.subheader("📊 Smart Digest")
if st.button("🧠 Generate Summary"):
    st.markdown(handle_command("smart digest"))

st.caption("Made with ❤️ using OpenAI + Streamlit")
