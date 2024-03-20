from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.conf import settings
import os.path
import json


class GoogleCalendar:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ]

    def __init__(self, credentials_file=settings.GOOGLE_TOKEN) -> None:
        self.creds = self.get_creds(credentials_file)
        self.service = build(
            "calendar", "v3", credentials=self.creds, cache_discovery=False
        )

    def get_creds(self, credentials_file):
        if os.path.exists(credentials_file):
            creds = Credentials.from_authorized_user_file(credentials_file, self.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        settings.GOOGLE_CREDENTIALS, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CREDENTIALS, self.SCOPES
            )
            creds = flow.run_local_server(port=0)
            with open(credentials_file, "w") as token:
                token.write(creds.to_json())
        return creds

    def get_calendars_list(self):
        return self.service.calendarList().list().execute().get("items", [])

    def get_events(self, cal_id="primary"):
        return self.service.events().list(calendarId=cal_id).execute().get("items", [])
