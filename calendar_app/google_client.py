from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.conf import settings
import os.path
import json


class GoogleCalendar:
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(self, company) -> None:
        self.credentials = self.get_credentials(company)
        self.service = build("calendar", "v3", credentials=self.credentials)

    def get_credentials(self, company):
        creds = None
        if company.google_token:
            creds = Credentials(company.google_token)
        elif company.credentials:
            creds = Credentials.from_authorized_user_info(
                json.loads(company.credentials), self.SCOPES
            )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CREDENTIALS, self.SCOPES
                )
                creds = flow.run_local_server(port=0, open_browser=False)
        return creds

    def get_calendars_list(self):
        return self.service.calendarList().list().execute().get("items", [])

    def get_events(self, cal_id="primary"):
        return self.service.events().list(calendarId=cal_id).execute().get("items", [])
