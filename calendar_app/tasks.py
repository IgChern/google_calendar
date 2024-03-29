import imp
import logging

from celery import group, shared_task
from django.conf import settings
from django.utils import timezone

from .google_client import GoogleCalendar
from .models import Company, Event, Hall

logger = logging.getLogger("celery_tasks")


@shared_task(bind=True)
def sync_company_calendars(self):
    company_tasks = []
    for company in Company.objects.all():
        company.last_update = timezone.now()
        company.save()
        task = update_halls_and_events.apply_async(
            kwargs={"company_id": company.pk},
            time_limit=settings.IMPORT_TIME,
        )
        company_tasks.append(task)
        logger.info(f"Updating halls for company: {company.name}")
    group(*company_tasks).apply_async()


@shared_task
def update_halls_and_events(company_id=None):
    api = GoogleCalendar()
    company = Company.objects.get(pk=company_id)
    company.update_company(api)
    company.last_update = timezone.now()
    company.save()
    halls = Hall.objects.filter(hall_company=company)
    logger.info(f"Updating halls for company: {company.name}")

    for hall in halls:
        hall.update_hall(api)
        hall.last_update = timezone.now()
        hall.save()
        logger.info(f"Updating hall: {hall.name}")

        events = Event.objects.filter(event_hall=hall)

        for event in events:

            event.check_overlapping_events()
            event.last_update = timezone.now()
            event.save()
            logger.info(f"Checking overlapping events for event: {event.google_id}")
