from .models import Company, Hall, Event
from .google_client import GoogleCalendar
from datetime import datetime


def sync_google_calendar_events():
    companies = Company.objects.all()

    for company in companies:
        google_calendar = company.get_google_calendar_obj()
        halls = Hall.objects.filter(company=company)

        for hall in halls:
            # Получаем события из Google календаря для данного зала
            google_events = google_calendar.get_events(cal_id=hall.google_calendar_id)

            for google_event in google_events:
                # Проверяем, существует ли событие в базе данных
                event_exists = Event.objects.filter(
                    google_id=google_event["id"]
                ).exists()

                if not event_exists:
                    # Если события нет в базе данных, добавляем его
                    start_time = datetime.strptime(
                        google_event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S%z"
                    )
                    end_time = datetime.strptime(
                        google_event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S%z"
                    )

                    Event.objects.create(
                        company=company,
                        hall=hall,
                        google_id=google_event["id"],
                        date_start=start_time,
                        date_end=end_time,
                    )

    print("Синхронизация завершена.")
