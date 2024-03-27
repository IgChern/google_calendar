from django.contrib import admin

from .models import Company, Event, Hall


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = (
        "hall_company",
        "name",
        "google_calendar_id",
    )
    list_filter = ("hall_company",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_company",
        "event_hall",
        "google_id",
        "date_start",
        "date_end",
        "error",
    )
    list_filter = ("event_company", "event_hall")
