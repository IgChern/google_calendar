from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event


"""
events = Event.objects.select_related('company', 'hall').filter(...)

for event in events:
    print(event.company.name)  # Доступ к связанным объектам без дополнительных запросов
    print(event.hall.name)

"""


@receiver(post_save, sender=Event)
def handle_event_save(sender, instance, created, **kwargs):
    if created:
        intersect_events = Event.objects.filter(
            hall=instance.hall,
            date_start__lt=instance.date_end,
            date_end__gt=instance.date_start,
        )

        if intersect_events.exists():
            intersect_events.update(error=1)
        else:
            instance.error = None
            instance.save()

    else:
        # Если событие было изменено, проверяем, изменился ли идентификатор календаря
        if instance.google_id != instance._old_google_id:
            # Если идентификатор календаря изменился, обновляем его в базе данных
            instance.hall.google_calendar_id = instance.google_calendar_id
            instance.hall.save(update_fields=["google_calendar_id"])
