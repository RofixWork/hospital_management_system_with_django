from django.contrib import admin

from .models import Doctor, Notification

# Register your models here.


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "mobile", "next_available_appointment_date"]
    search_fields = ["full_name", "mobile"]
    list_filter = ["next_available_appointment_date"]
    list_display_links = ["full_name"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "doctor", "date", "is_seen", "type"]
    search_fields = ["doctor__full_name", "doctor__mobile"]
    list_filter = ["date", "is_seen", "type"]
