from django.db import models
from django.utils.translation import gettext_lazy as _
from .google_client import GoogleCalendar
from django.contrib.auth.models import User
from .google_client import GoogleCalendar


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

    def make_halls_calendars(self, api: GoogleCalendar):
        response_list = api.get_calendars_list()
        for calendar in response_list:
            hall, created = Hall.objects.get_or_create(
                company=self.company, google_calendar_id=calendar["id"]
            )
            hall.name = calendar.get("summary")
            hall.google_calendar_id = calendar.get("id")
            hall.save()


class Event(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_events"
    )
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="hall_events")
    google_id = models.CharField(_("event ID"), max_length=255, blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    error = models.BooleanField(default=None)

    def __str__(self):
        return f"{self.hall} - {self.date_start} - {self.date_end}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_google_id = self.google_id

    def save(self, *args, **kwargs):
        if self.google_id != self._old_google_id:
            self._old_google_id = self.google_id
        super().save(*args, **kwargs)

    def make_halls_events(self, api: GoogleCalendar):
        response_list = api.get_events(self.hall.google_calendar_id)
        for event in response_list:
            event_obj, created = Event.objects.get_or_create(
                company=self.company,
                hall=self.hall,
                google_id=event["id"],
            )
            if (
                created
                or event_obj.date_start != event["start"].get("dateTime")
                or event_obj.date_end != event["end"].get("dateTime")
            ):
                event_obj.date_start = event["start"].get("dateTime")
                event_obj.date_end = event["end"].get("dateTime")
                event_obj.save()
