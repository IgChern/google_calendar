from celery import shared_task
from .models import Company, Hall, Event
from .google_client import GoogleCalendar
from .helpers import save_events_to_database


@shared_task
def update_halls_and_events():
    try:
        companies = Company.objects.all()

        for company in companies:
            api = GoogleCalendar(company)
            halls = Hall.objects.filter(company=company)
            for hall in halls:
                hall.make_halls_calendars(api)
                events = Event.objects.filter(company=company, hall=hall)
                for event in events:
                    event.make_halls_events(api)

    except Exception as e:
        print(f"Error updating halls and events: {e}")
