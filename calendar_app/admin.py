from django.contrib import admin
from .models import (
    Company,
    Hall,
    Event,
)


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "name",
        "google_calendar_id",
    )
    list_filter = ("company",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("company", "hall", "google_id", "date_start", "date_end", "error")
    list_filter = ("company", "hall")
