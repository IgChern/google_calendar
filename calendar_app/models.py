from django.db import models
from django.utils.translation import gettext_lazy as _
from .google_client import GoogleCalendar
from django.contrib.auth.models import User
from django.db.models.query_utils import Q


# Create your models here.


class Company(models.Model):
    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE, default=""
    )
    name = models.CharField(_("Company Name"), max_length=255)
    google_token = models.CharField(_("Google Token"), max_length=255, blank=True)
    credentials = models.TextField(_("Credentials"), null=True, blank=True)

    def __str__(self):
        return self.name

    def update_company(self, api: GoogleCalendar):
        try:
            response_list = api.get_calendars_list()
            for calendar in response_list:
                hall, created = Hall.objects.get_or_create(
                    company=self,
                    name=calendar["summary"],
                    google_calendar_id=calendar["id"],
                )
                hall.save
        except Exception as e:
            print(f"Error updating company {self.name}: {e}")


class Hall(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_halls"
    )
    name = models.CharField(_("Hall name"), max_length=255)
    google_calendar_id = models.CharField(
        _("Google calendar ID"), max_length=255, blank=True
    )

    def __str__(self):
        return self.name

    def update_hall(self, api: GoogleCalendar):
        try:
            response_list = api.get_events(self.google_calendar_id)
            for event in response_list:
                event_obj, created = Event.objects.get_or_create(
                    hall=self,
                    company=self.company,
                    google_id=event["id"],
                    defaults={
                        "date_start": event["start"].get("dateTime"),
                        "date_end": event["end"].get("dateTime"),
                    },
                )
                if not created:
                    event_obj.company = self.company
                    event_obj.hall = self
                    event_obj.google_id = event["id"]
                    if (
                        event_obj.date_start is not None
                        and event_obj.date_end is not None
                    ):
                        event_obj.date_start = event["start"].get("dateTime")
                        event_obj.date_end = event["end"].get("dateTime")
                event_obj.save()
        except Exception as e:
            print(f"Error updating hall {self.name}: {e}")


class Event(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_events"
    )
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="hall_events")
    google_id = models.CharField(_("event ID"), max_length=255, blank=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    error = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.hall} - {self.date_start} - {self.date_end}"

    def save(self, *args, **kwargs):
        # self.check_overlapping_events()
        super().save(*args, **kwargs)

    def check_overlapping_events(self):
        events = Event.objects.filter(hall=self.hall).order_by("date_start")
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
                    self.error = 1

            active_events.append(event)

        Event.objects.filter(pk__in=[event.pk for event in overlapping_events]).update(
            error=1
        )
