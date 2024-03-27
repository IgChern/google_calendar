from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .google_client import GoogleCalendar


class GoogleModel(models.Model):
    last_update = models.DateTimeField(_("Last Update"), null=True, blank=True)
    sync_token = models.CharField(
        _("Sync Token"), blank=True, default="", max_length=255
    )


class Company(GoogleModel):
    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE, default=""
    )
    name = models.CharField(_("Company Name"), max_length=255)

    def update_company(self, api: GoogleCalendar):
        try:
            response_list = api.get_calendars_list()
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

    def update_hall(self, api: GoogleCalendar):
        try:
            response_list = api.get_events(self.google_calendar_id)
            for event in response_list.get("items", []):
                event_obj, created = Event.objects.get_or_create(
                    event_hall=self,
                    event_company=self.hall_company,
                    google_id=event["id"],
                    defaults={
                        "date_start": event["start"].get("dateTime"),
                        "date_end": event["end"].get("dateTime"),
                    },
                )
                if not created:
                    event_obj.event_company = self.hall_company
                    event_obj.event_hall = self
                    event_obj.google_id = event["id"]
                    if (
                        event_obj.date_start is not None
                        and event_obj.date_end is not None
                    ):
                        event_obj.date_start = event["start"].get("dateTime")
                        event_obj.date_end = event["end"].get("dateTime")
                event_obj.save()

            sync_token = response_list.get("nextSyncToken", "")
            self.sync_token = sync_token
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
    error = models.IntegerField(default=0)

    def check_overlapping_events(self):
        events = Event.objects.filter(event_hall=self.event_hall).order_by("date_start")
        events.update(error=0)

        active_events = []
        overlapping_events = []
        for event in events:
            active_events = [
                ev for ev in active_events if ev.date_end > event.date_start
            ]

            for active_event in active_events:
                if event.date_end > active_event.date_start:
                    overlapping_events.append(event)
                    overlapping_events.append(active_event)

            active_events.append(event)

        Event.objects.filter(pk__in=[event.pk for event in overlapping_events]).update(
            error=1
        )

    def __str__(self):
        return f"{self.event_hall} - {self.date_start} - {self.date_end}"

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
