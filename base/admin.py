from django.contrib import admin

from .models import Appointment, LabTest, MedicalRecord, Prescription, Service

# Register your models here.


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "cost"]
    search_fields = ["name"]
    list_filter = ["cost"]
    list_display_links = ["name"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["id", "patient", "doctor", "status"]
    list_display_links = ["id"]
    search_fields = ["patient__full_name", "doctor__full_name"]
    list_filter = ["status"]


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ["appointment", "id", "test_name", "result"]
    search_fields = ["test_name"]
    list_filter = ["result"]
    list_display_links = ["appointment", "test_name"]


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ["appointment", "id", "diagnosis"]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["appointment", "id", "medications"]
