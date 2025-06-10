import openai
import json
import re
from datetime import datetime
import dateparser
from dateutil import parser as dateutil_parser

from task_manager import (
    add_task, view_tasks, delete_task, clear_all_tasks, get_smart_digest, load_tasks
)
from calendar_sync import create_google_event

openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ this is safe


def normalize_due_date(due):
    try:
        if not due:
            return None

        if isinstance(due, dict):
            combined = f"{due.get('date', '')} {due.get('time', '')}".strip()
        elif isinstance(due, str):
            combined = due.strip()
        else:
            return None

        combined = re.sub(r"next week (\w+)", r"next \1", combined, flags=re.IGNORECASE)
        combined = re.sub(r"\bat\b", "", combined, flags=re.IGNORECASE).strip()

        parsed = dateparser.parse(combined, settings={"PREFER_DATES_FROM": "future"})

        if not parsed:
            try:
                parsed = dateutil_parser.parse(combined, fuzzy=True)
            except Exception:
                parsed = None

        if parsed:
            formatted = parsed.strftime("%Y-%m-%d %I:%M %p") if parsed.time() != datetime.min.time() else parsed.strftime("%Y-%m-%d")
            print("\U0001F4C6 Normalized Due Date:", formatted)
            return formatted

        print(f"\u26A0\uFE0F Failed to parse date: '{combined}'")
        return None

    except Exception as e:
        print(f"\u26A0\uFE0F Error in normalize_due_date: {e}")
        return None

def handle_command(command):
    command_lower = command.lower()

    if "show tasks" in command_lower:
        return view_tasks()

    match = re.search(r"delete task (\d+)", command_lower)
    if match:
        index = int(match.group(1)) - 1
        return delete_task(index)

    if "clear all tasks" in command_lower:
        return clear_all_tasks()

    if "daily digest" in command_lower or "smart digest" in command_lower:
        return get_smart_digest()

    match_sync = re.search(r"(sync|add) task (\d+) to calendar", command_lower)
    if match_sync:
        task_index = int(match_sync.group(2)) - 1
        tasks = load_tasks()
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            link = create_google_event(task['description'], task['due_date'])
            return f"\U0001F4C5 Task synced to Google Calendar: {link}" if link else "❌ Failed to sync to calendar."
        return "❌ Invalid task number."

    prompt = f"""
    Extract the main task, category (Work/Personal/Health), and due date from this text:
    \"{command}\".
    Return a JSON with keys: description, category, due_date. If any field is missing, use null.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You extract structured task info from user messages."},
                {"role": "user", "content": prompt}
            ]
        )
        gpt_output = response.choices[0].message.content.strip()
        print("\U0001F50D GPT Output:\n", gpt_output)

        try:
            parsed = json.loads(gpt_output)
        except json.JSONDecodeError:
            return "❌ Sorry, I couldn't understand the response format. Please try rephrasing."

        if not parsed.get("description"):
            return "❌ Sorry, I couldn't understand the task. Please rephrase it clearly."

        raw_due = parsed.get("due_date")
        normalized_due = normalize_due_date(raw_due)
        if not normalized_due:
            return f"❌ Sorry, I couldn't understand the due date: {raw_due}"

        parsed["due_date"] = normalized_due
        added, conflict_msg = add_task(parsed['description'], parsed.get('category'), parsed["due_date"])

        message = f"✅ Task added: {added['description']} (Category: {added['category']})"
        if conflict_msg:
            message += f"\n⚠️ Conflict: {conflict_msg}"
        return message

    except Exception as e:
        return f"❌ Error: {str(e)}"
