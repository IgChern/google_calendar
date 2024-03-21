from celery import shared_task
from .models import Company, Hall
from .google_client import GoogleCalendar
from .helpers import save_events_to_database


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
            for hall in halls:
                hall.update_hall(api)

    except Exception as e:
        print(f"Ошибка при обновлении залов и событий: {e}")
