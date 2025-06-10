import json
from datetime import datetime, timedelta
import os
import dateparser

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("⚠️ Warning: Corrupted tasks.json, resetting.")
        return []

def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save tasks: {e}")

def add_task(description, category="General", due_date=None):
    tasks = load_tasks()

    if not description:
        return None, "Description cannot be empty."

    task = {
        "description": description.strip(),
        "category": category or "General",
        "due_date": due_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }

    conflict_tasks = check_for_conflicts(due_date, tasks)

    tasks.append(task)
    save_tasks(tasks)

    if conflict_tasks:
        conflict_msg = "\n⚠️ Conflict(s) detected:\n"
        for c in conflict_tasks:
            conflict_msg += f"- {c['description']} (Due: {c['due_date']})\n"
        return task, conflict_msg.strip()

    return task, None

def view_tasks(return_as_list=False):
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    if return_as_list:
        return tasks

    if not tasks:
        return "📭 No tasks found."

    output = []
    for i, task in enumerate(tasks, start=1):
        output.append(f"{i}. {task['description']} [Category: {task['category']}] (Due: {task['due_date']})")
    return "VocalMate: " + "\n".join(output)


def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        return f"🗑️ Deleted task: {removed['description']}"
    return "❌ Invalid task number."

def clear_all_tasks():
    save_tasks([])
    return "✅ All tasks cleared."

def check_for_conflicts(new_due, tasks):
    new_dt = dateparser.parse(new_due)
    if not new_dt:
        return []

    conflicts = []
    for task in tasks:
        existing_due = task.get("due_date")
        if existing_due:
            existing_dt = dateparser.parse(existing_due)
            if existing_dt and abs((new_dt - existing_dt).total_seconds()) < 3 * 3600:
                conflicts.append(task)
    return conflicts

def get_smart_digest():
    tasks = load_tasks()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    digest = {
        "today": [],
        "tomorrow": []
    }

    for task in tasks:
        due_str = task.get("due_date")
        if due_str:
            due_parsed = dateparser.parse(due_str)
            if due_parsed:
                if due_parsed.date() == today:
                    digest["today"].append(task)
                elif due_parsed.date() == tomorrow:
                    digest["tomorrow"].append(task)

    if not digest["today"] and not digest["tomorrow"]:
        return "📭 No tasks due today or tomorrow."

    result = "📅 Smart Daily Digest:\n"
    if digest["today"]:
        result += "\n🟢 **Today:**\n"
        for t in digest["today"]:
            result += f"- {t['description']} (Category: {t.get('category')})\n"
    if digest["tomorrow"]:
        result += "\n🟡 **Tomorrow:**\n"
        for t in digest["tomorrow"]:
            result += f"- {t['description']} (Category: {t.get('category')})\n"

    return result.strip()
