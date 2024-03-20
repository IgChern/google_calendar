from .models import Event


def save_events_to_database(events, company, hall):
    for event_data in events:
        google_id = event_data.get("id")
        date_start = event_data.get("start").get("dateTime")
        date_end = event_data.get("end").get("dateTime")

        existing_event = Event.objects.filter(google_id=google_id, hall=hall).first()
        if existing_event:

            existing_event.date_start = date_start
            existing_event.date_end = date_end
            existing_event.save()
        else:
            new_event = Event.objects.create(
                company=company,
                hall=hall,
                google_id=google_id,
                date_start=date_start,
                date_end=date_end,
            )
