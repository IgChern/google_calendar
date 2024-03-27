import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleEntry:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ]

    def __init__(self, credentials_file="calendar_app/credentials/token.json") -> None:
        self.creds = self.get_creds(credentials_file)
        self.service = build(
            "calendar", "v3", credentials=self.creds, cache_discovery=False
        )

    def get_creds(self, credentials_file):
        if os.path.exists(credentials_file):
            creds = Credentials.from_authorized_user_file(credentials_file, self.SCOPES)
        else:
            creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "calendar_app/credentials/credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("calendar_app/credentials/token.json", "w") as token:
                token.write(creds.to_json())

        return creds


obj = GoogleEntry()
