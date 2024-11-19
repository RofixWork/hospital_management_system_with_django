from django.contrib import admin

from .models import Notification, Patient

# Register your models here.


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "full_name", "email"]
    search_fields = ["full_name", "email"]
    list_filter = ["gender"]
    list_display_links = ["user", "full_name"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "patient", "date", "is_seen", "type"]
    search_fields = ["patient__full_name", "patient__email"]
