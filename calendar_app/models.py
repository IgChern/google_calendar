from dateutil.parser import parse
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .google_client import GoogleCalendar


class GoogleModel(models.Model):
    last_update = models.DateTimeField(_("Last Update"), null=True, blank=True)
    sync_token = models.CharField(
        _("Sync Token"), blank=True, default="", max_length=255
    )
    page_token = models.CharField(
        _("Page Token"), blank=True, default="", max_length=255
    )


class Company(GoogleModel):
    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE, default=""
    )
    name = models.CharField(_("Company Name"), max_length=255)

    def update_company(self, api: GoogleCalendar, page_token=None):
        try:
            response_list = api.get_calendars_list(
                sync_token=self.sync_token, page_token=self.page_token
            )
            for calendar in response_list.get("items", []):
                hall, created = Hall.objects.get_or_create(
                    hall_company=self,
                    name=calendar["summary"],
                    google_calendar_id=calendar["id"],
                )
                hall.save

            sync_token = response_list.get("nextSyncToken", "")
            self.sync_token = sync_token
            self.save()

            page_token = response_list.get("nextPageToken", None)
            if page_token is not None:
                self.page_token = page_token
                self.save()

        except Exception as e:
            print(f"Error updating company {self.name}: {e}")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


class Hall(GoogleModel):
    hall_company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_halls"
    )
    name = models.CharField(_("Hall name"), max_length=255)
    google_calendar_id = models.CharField(
        _("Google calendar ID"), max_length=255, blank=True
    )

    def update_hall(self, api: GoogleCalendar, page_token=None):
        try:
            response_list = api.get_events(
                cal_id=self.google_calendar_id,
                sync_token=self.sync_token,
                page_token=self.page_token,
            )
            for event in response_list.get("items", []):

                start_time = event["start"].get("dateTime")
                end_time = event["end"].get("dateTime")
                event_etag = event["etag"]

                event_obj, created = Event.objects.update_or_create(
                    event_hall=self,
                    google_id=event["id"],
                    defaults={
                        "event_company": self.hall_company,
                        "date_start": start_time,
                        "date_end": end_time,
                        "etag": event_etag,
                    },
                )

                if created or event_obj.etag != event_etag:
                    event_obj.etag = event_etag
                    event_obj.save()

            sync_token = response_list.get("nextSyncToken", "")
            self.sync_token = sync_token

            page_token = response_list.get("nextPageToken", None)
            if page_token is not None:
                self.page_token = page_token
            self.save()

        except Exception as e:
            print(f"Error updating hall {self.name}: {e}")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hall")
        verbose_name_plural = _("Halls")


class Event(GoogleModel):
    event_company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_events"
    )
    event_hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="hall_events"
    )
    google_id = models.CharField(_("Event ID"), max_length=255, blank=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    etag = models.CharField(_("etag"), max_length=255, blank=True)
    error = models.IntegerField(default=0)

    def check_overlapping_events(self):
        start_time = self.date_start
        end_time = self.date_end
        overlapping_events = Event.objects.filter(
            event_hall=self.event_hall,
            date_start__lt=end_time,
            date_end__gt=start_time,
        ).exclude(pk=self.pk)

        if overlapping_events.exists():
            self.error = 1
            overlapping_events.update(error=1)
        else:
            self.error = 0

        self.save()

    def __str__(self):
        return f"{self.event_hall} - {self.date_start} - {self.date_end}"

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        indexes = [
            models.Index(fields=["date_start", "date_end", "event_hall"]),
        ]
