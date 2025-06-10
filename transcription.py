# transcription.py

import openai
import json
from task_manager import add_task

# ✅ Use your actual OpenAI key (for testing only — remove before pushing to GitHub)
openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ this is safe


def transcribe_and_extract_tasks(file_path):
    try:
        print(f"🎧 Transcribing audio from file: {file_path} ...")
        
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            ).text

        print("\n📄 Transcript:\n", transcript)

        # 🔍 Prompt GPT to extract tasks
        prompt = f"""From the following meeting transcript, extract actionable tasks.
Return a JSON list of dictionaries with: description, category (Work/Personal/Health), and due_date (if mentioned).
Transcript:
\"\"\"
{transcript}
\"\"\"
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if enabled
            messages=[
                {"role": "system", "content": "You extract structured task lists from meeting transcripts."},
                {"role": "user", "content": prompt}
            ]
        )

        gpt_output = response.choices[0].message.content.strip()
        print("\n📌 Extracted Tasks JSON:\n", gpt_output)

        # ✅ Clean markdown code block if GPT returns ```json ... ```
        if "```json" in gpt_output:
            gpt_output = gpt_output.split("```json")[1]
        if "```" in gpt_output:
            gpt_output = gpt_output.split("```")[0]
        gpt_output = gpt_output.strip()

        # ✅ Parse and save tasks
        tasks = json.loads(gpt_output)

        for task in tasks:
            add_task(task['description'], task.get('category'), task.get('due_date'))

        return f"✅ {len(tasks)} task(s) added from transcript."

    except Exception as e:
        return f"❌ Error during transcription or task extraction: {e}"
