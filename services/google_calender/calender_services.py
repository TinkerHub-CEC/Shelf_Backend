from __future__ import print_function
import datetime
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event(event_obj):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    start_datetime = event_obj.start_datetime.utcnow().isoformat()
    end_datetime = event_obj.end_datetime.utcnow().isoformat()
    event = {
    'summary': f'{event_obj.title}',
    'location': 'College Of engineering, Chengannur',
    'description': f'{event_obj.title}',
    'start': {
        'dateTime': f'{start_datetime}',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': f'{end_datetime}',
        'timeZone': 'America/Los_Angeles',
    },
    'attendees': [
        {'email': 'tinkerhubshelf@gmail.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    
    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    return event.get('id')
    
def update_event(event_obj, user_email):
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = service.events().get(calendarId='primary', eventId=event_obj.calender_event_id ).execute()
    event['attendees'].append(user_email)

    service.events().update(calendarId='primary', eventId=event['id'], body=event, sendUpdates='all').execute()
