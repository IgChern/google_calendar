import logging

from django.conf import settings
from googleapiclient.discovery import build

from calendar_app.credentials.oauth2 import GoogleEntry

logger = logging.getLogger("django_app")


class GoogleCalendar(GoogleEntry):
    SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ]

    def __init__(self, credentials_file=settings.GOOGLE_TOKEN) -> None:
        self.creds = self.get_creds(credentials_file)
        self.service = build(
            "calendar", "v3", credentials=self.creds, cache_discovery=False
        )

    def get_calendars_list(self, sync_token=None, page_token=None):
        response = (
            self.service.calendarList()
            .list(syncToken=sync_token, pageToken=page_token)
            .execute()
        )
        logger.info(response)
        return response

    def get_events(self, cal_id, sync_token=None, page_token=None):
        response = (
            self.service.events()
            .list(calendarId=cal_id, syncToken=sync_token, pageToken=page_token)
            .execute()
        )
        logger.info(response)
        return response
