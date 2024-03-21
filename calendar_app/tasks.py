from celery import shared_task
from .models import Company, Hall, Event
from .google_client import GoogleCalendar
import logging

logger = logging.getLogger("celery_tasks")
logger.propagate = False


@shared_task
def update_halls_and_events(max_companies=None):
    try:
        api = GoogleCalendar()
        if max_companies:
            companies = Company.objects.all()[:max_companies]
        else:
            companies = Company.objects.all()

        for company in companies:
            company.update_company(api)
            halls = Hall.objects.filter(company=company)
            logger.info(f"Updating halls for company: {company.name}")
            for hall in halls:
                hall.update_hall(api)
                logger.info(f"Updating hall: {hall.name}")
                events = Event.objects.filter(hall=hall)
                for event in events:
                    event.check_overlapping_events()
                    logger.info(
                        f"Checking overlapping events for event: {event.google_id}"
                    )

    except Exception as e:
        print(f"Ошибка при обновлении залов и событий: {e}")
