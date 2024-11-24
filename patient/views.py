from typing import Any

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView

from base.models import (
    APPOINTMENT_TYPE,
    Appointment,
    Billing,
    LabTest,
    MedicalRecord,
    Prescription,
)
from utils.mixins import CheckUserIsPatientContextMixin

from .forms import UpdatePatientForm
from .models import Notification as PatientNotification
from .models import Patient


# Create your views here.
class PatientDashboardView(
    LoginRequiredMixin, CheckUserIsPatientContextMixin, ListView
):
    template_name = "patient/dashboard.html"
    model = Appointment
    context_object_name = "appointments"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        notifications_count = PatientNotification.objects.filter(
            patient=self.patient
        ).count()
        appointments_count = Appointment.objects.filter(patient=self.patient).count()
        total_spent = Billing.objects.filter(patient=self.patient).aggregate(
            total_spent=models.Sum("total", default=0)
        )["total_spent"]
        context["notifications_count"] = notifications_count
        context["appointments_count"] = appointments_count
        context["total_spent"] = total_spent
        return context

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.patient)


class PatientAppointmentsView(
    LoginRequiredMixin, CheckUserIsPatientContextMixin, ListView
):
    template_name = "patient/appointments.html"
    model = Appointment
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.patient)


class AppointmentDetailsView(
    LoginRequiredMixin, CheckUserIsPatientContextMixin, DetailView
):
    template_name = "patient/appointment_details.html"
    model = Appointment

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["medical_records"] = MedicalRecord.objects.filter(
            appointment=self.get_object()
        )
        context["lab_tests"] = LabTest.objects.filter(appointment=self.get_object())
        context["prescriptions"] = Prescription.objects.filter(
            appointment=self.get_object()
        )
        return context

    def get_object(self, queryset=None):
        appointment_id = self.kwargs.get("pk")
        return Appointment.objects.get(
            patient=self.patient, appointment_id=appointment_id
        )


class PatientCompleteAppointment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "patient"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.patient = request.user.patient
        appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, patient=self.patient
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.appointment.status = APPOINTMENT_TYPE.COMPLETED
        self.appointment.save()

        messages.success(request, "Appointment completed successfully.")
        return redirect(
            reverse(
                "patient_appointment_details",
                kwargs={"pk": self.appointment.appointment_id},
            )
        )


class PatientCancelledAppointment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "patient"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.patient = request.user.patient
        appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, patient=self.patient
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.appointment.status = APPOINTMENT_TYPE.CANCELLED
        self.appointment.save()

        messages.success(request, "Appointment Cancelled successfully.")
        return redirect(
            reverse(
                "patient_appointment_details",
                kwargs={"pk": self.appointment.appointment_id},
            )
        )


class PatientActivatedAppointment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "patient"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.patient = request.user.patient
        appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, patient=self.patient
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.appointment.status = APPOINTMENT_TYPE.SCHEDULED
        self.appointment.save()

        messages.success(request, "Appointment re activate successfully.")
        return redirect(
            reverse(
                "patient_appointment_details",
                kwargs={"pk": self.appointment.appointment_id},
            )
        )


class PatientPaymentsView(LoginRequiredMixin, CheckUserIsPatientContextMixin, ListView):
    model = Billing
    template_name = "patient/payments.html"
    context_object_name = "billings"

    def get_queryset(self):
        return Billing.objects.filter(appointment__patient=self.patient)


class PatientNotificationsView(
    LoginRequiredMixin, CheckUserIsPatientContextMixin, ListView
):
    model = PatientNotification
    template_name = "patient/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return PatientNotification.objects.filter(patient=self.patient, is_seen=False)


class PatientMarkSeenNotificationView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "patient"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.patient = request.user.patient
        notification_id = self.kwargs.get("notification_id")
        self.notification = get_object_or_404(
            PatientNotification, id=notification_id, patient=self.patient
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.notification.is_seen = True
        self.notification.save()
        messages.success(request, "Notification marked as seen.")
        return redirect(reverse("patient_notifications"))


class PatientProfileView(
    LoginRequiredMixin, CheckUserIsPatientContextMixin, UpdateView
):
    template_name = "patient/profile.html"
    form_class = UpdatePatientForm
    success_url = reverse_lazy("patient_profile")

    def form_valid(self, form):
        # message success update doctor info
        messages.success(self.request, "Patient profile updated successfully.")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Patient, user=self.request.user)
