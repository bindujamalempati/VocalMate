from datetime import datetime, timedelta
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 👇 Scope required to access the user's primary calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_google_event(description, due_date_str):
    try:
        # ⏰ Parse due_date_str (assumes format: "YYYY-MM-DD HH:MM AM/PM")
        start_time = datetime.strptime(due_date_str, "%Y-%m-%d %I:%M %p")
        end_time = start_time + timedelta(hours=1)

        creds = None
        # ✅ Use cached token if it exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        else:
            # 🔐 Perform OAuth2 flow
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # 🔧 Build Calendar API service
        service = build('calendar', 'v3', credentials=creds)

        # 📅 Define the event
        event = {
            'summary': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/New_York',
            },
        }

        # 🚀 Insert event into calendar
        created_event = service.events().insert(calendarId='primary', body=event).execute()

        event_link = created_event.get('htmlLink')
        print(f"📅 Google Calendar Event Created: {event_link}")
        return event_link

    except Exception as e:
        print(f"⚠️ Calendar sync error: {e}")
        return None
