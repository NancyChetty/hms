import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')


def get_service():

    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def create_event(doctor_email, patient_email, start_time, end_time):

    service = get_service()

    event = {
        'summary': 'Doctor Appointment',
        'location': 'MediCare Hospital',
        'description': (
            f'Appointment confirmed.\n\n'
            f'Doctor: {doctor_email}\n'
            f'Patient: {patient_email}'
        ),
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [
            {'email': doctor_email},
            {'email': patient_email},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 30},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    created = service.events().insert(
        calendarId='primary',
        body=event,
        sendUpdates='all'
    ).execute()

    return created.get('id')


def delete_event(event_id):

    if not event_id:
        return

    service = get_service()

    service.events().delete(
        calendarId='primary',
        eventId=event_id,
        sendUpdates='all'
    ).execute()
