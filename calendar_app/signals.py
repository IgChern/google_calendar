from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event


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
        if instance.google_id != instance._old_google_id:
            instance.hall.google_calendar_id = instance.google_calendar_id
            instance.hall.save(update_fields=["google_calendar_id"])
