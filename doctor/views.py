from typing import Any

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from base.models import (
    APPOINTMENT_TYPE,
    Appointment,
    Billing,
    LabTest,
    MedicalRecord,
    Prescription,
)
from utils.mixins import CheckUserIsADoctorDispatchMixin, CheckUserIsDoctorContextMixin

from .forms import UpdateDoctorForm
from .models import Doctor
from .models import Notification as DoctorNotification

# Create your views here.


class DoctorDashboardView(LoginRequiredMixin, CheckUserIsDoctorContextMixin, ListView):
    template_name = "doctor/dashboard.html"
    model = Appointment
    context_object_name = "appointments"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["notifications"] = DoctorNotification.objects.filter(
            doctor=self.doctor
        ).count()
        return context

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.doctor)


class DoctorAppointmentsView(
    LoginRequiredMixin, CheckUserIsDoctorContextMixin, ListView
):
    template_name = "doctor/appointments.html"
    model = Appointment
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.doctor)


class AppointmentDetailsView(
    LoginRequiredMixin, CheckUserIsDoctorContextMixin, DetailView
):
    template_name = "doctor/appointment_details.html"
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
            doctor=self.doctor, appointment_id=appointment_id
        )


class DoctorCreateMedicalRecordView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        self.appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, doctor=self.doctor, appointment_id=self.appointment_id
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):

        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")

        # handle empty fields
        if not diagnosis.strip() or not treatment.strip():
            messages.error(request, "Please fill out all required fields.")
            return redirect(
                reverse(
                    "doctor_appointment_details", kwargs={"pk": self.appointment_id}
                )
            )
        MedicalRecord.objects.create(
            appointment=self.appointment, diagnosis=diagnosis, treatment=treatment
        )
        messages.success(request, "Medical record created successfully.")

        return redirect(
            reverse("doctor_appointment_details", kwargs={"pk": self.appointment_id})
        )


class DoctorEditMedicalRecordView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        self.appointment_id = self.kwargs.get("appointment_id")
        self.medical_record_id = self.kwargs.get("medical_record_id")
        self.appointment = get_object_or_404(
            Appointment, doctor=self.doctor, appointment_id=self.appointment_id
        )
        self.medical_record = get_object_or_404(
            MedicalRecord,
            appointment=self.appointment,
            id=self.medical_record_id,
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")

        # handle empty fields
        if not diagnosis.strip() or not treatment.strip():
            # give me a error message nice
            messages.error(request, "Please fill out all required fields.")

            return redirect(
                reverse(
                    "doctor_appointment_details", kwargs={"pk": self.appointment_id}
                )
            )
        self.medical_record.diagnosis = diagnosis
        self.medical_record.treatment = treatment
        self.medical_record.save()
        messages.success(request, "Medical record updated successfully.")
        return redirect(
            reverse("doctor_appointment_details", kwargs={"pk": self.appointment_id})
        )


class DoctorCreateLabTestView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        self.appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, doctor=self.doctor, appointment_id=self.appointment_id
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):

        test_name = request.POST.get("test_name")
        description = request.POST.get("description")
        result = request.POST.get("result")

        # handle empty fields
        if not test_name.strip() or not description.strip() or not result.strip():
            messages.error(request, "Please fill out all required fields.")
            return redirect(
                reverse(
                    "doctor_appointment_details", kwargs={"pk": self.appointment_id}
                )
            )

        LabTest.objects.create(
            appointment=self.appointment,
            test_name=test_name,
            description=description,
            result=result,
        )

        messages.success(request, "Lab Test created successfully.")

        return redirect(
            reverse("doctor_appointment_details", kwargs={"pk": self.appointment_id})
        )


class DoctorEditLabTestView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        self.appointment_id = self.kwargs.get("appointment_id")
        self.lab_test_id = self.kwargs.get("lab_test_id")
        self.appointment = get_object_or_404(
            Appointment, doctor=self.doctor, appointment_id=self.appointment_id
        )
        self.lab_test = get_object_or_404(
            LabTest,
            appointment=self.appointment,
            id=self.lab_test_id,
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        test_name = request.POST.get("test_name")
        description = request.POST.get("description")
        result = request.POST.get("result")

        # handle empty fields
        if not test_name.strip() or not description.strip() or not result.strip():
            # give me a error message nice
            messages.error(request, "Please fill out all required fields.")

            return redirect(
                reverse(
                    "doctor_appointment_details", kwargs={"pk": self.appointment_id}
                )
            )

        self.lab_test.test_name = test_name
        self.lab_test.description = description
        self.lab_test.result = result
        self.lab_test.save()
        messages.success(request, "Lab Test updated successfully.")
        return redirect(
            reverse("doctor_appointment_details", kwargs={"pk": self.appointment_id})
        )


class DoctorCreatePrescriptionView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        self.appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, doctor=self.doctor, appointment_id=self.appointment_id
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):

        medications = request.POST.get("medications")

        # handle empty fields
        if not medications.strip():
            messages.error(request, "Please fill out all required fields.")
            return redirect(
                reverse(
                    "doctor_appointment_details", kwargs={"pk": self.appointment_id}
                )
            )

        Prescription.objects.create(
            appointment=self.appointment, medications=medications
        )

        messages.success(request, "Prescription created successfully.")

        return redirect(
            reverse("doctor_appointment_details", kwargs={"pk": self.appointment_id})
        )


class DoctorEditPrescriptionView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        self.appointment_id = self.kwargs.get("appointment_id")
        self.prescription_id = self.kwargs.get("prescription_id")
        self.appointment = get_object_or_404(
            Appointment, doctor=self.doctor, appointment_id=self.appointment_id
        )
        self.prescription = get_object_or_404(
            Prescription,
            appointment=self.appointment,
            id=self.prescription_id,
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        medications = request.POST.get("medications")

        # handle empty fields
        if not medications.strip():
            # give me a error message nice
            messages.error(request, "Please fill out all required fields.")

            return redirect(
                reverse(
                    "doctor_appointment_details", kwargs={"pk": self.appointment_id}
                )
            )

        self.prescription.medications = medications
        self.prescription.save()
        messages.success(request, "Prescription updated successfully.")
        return redirect(
            reverse("doctor_appointment_details", kwargs={"pk": self.appointment_id})
        )


class DoctorCompleteAppointment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.doctor = request.user.doctor
        appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, doctor=self.doctor
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.appointment.status = APPOINTMENT_TYPE.COMPLETED
        self.appointment.save()

        messages.success(request, "Appointment completed successfully.")
        return redirect(
            reverse(
                "doctor_appointment_details",
                kwargs={"pk": self.appointment.appointment_id},
            )
        )


class DoctorCancelledAppointment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.doctor = request.user.doctor
        appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, doctor=self.doctor
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.appointment.status = APPOINTMENT_TYPE.CANCELLED
        self.appointment.save()

        messages.success(request, "Appointment Cancelled successfully.")
        return redirect(
            reverse(
                "doctor_appointment_details",
                kwargs={"pk": self.appointment.appointment_id},
            )
        )


class DoctorActivatedAppointment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.doctor = request.user.doctor
        appointment_id = self.kwargs.get("appointment_id")
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, doctor=self.doctor
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.appointment.status = APPOINTMENT_TYPE.SCHEDULED
        self.appointment.save()

        messages.success(request, "Appointment re activate successfully.")
        return redirect(
            reverse(
                "doctor_appointment_details",
                kwargs={"pk": self.appointment.appointment_id},
            )
        )


class DoctorPaymentsView(LoginRequiredMixin, CheckUserIsDoctorContextMixin, ListView):
    model = Billing
    template_name = "doctor/payments.html"
    context_object_name = "billings"

    def get_queryset(self):
        return Billing.objects.filter(appointment__doctor=self.doctor)


class DoctorNotificationsView(
    LoginRequiredMixin, CheckUserIsDoctorContextMixin, ListView
):
    model = DoctorNotification
    template_name = "doctor/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return DoctorNotification.objects.filter(doctor=self.doctor, is_seen=False)


class DoctorMarkSeenNotificationView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            # create error message
            messages.error(
                request, "You are not authorized to complete this appointment."
            )
            return redirect(reverse("auth.login"))
        self.doctor = request.user.doctor
        notification_id = self.kwargs.get("notification_id")
        self.notification = get_object_or_404(
            DoctorNotification, id=notification_id, doctor=self.doctor
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.notification.is_seen = True
        self.notification.save()
        messages.success(request, "Notification marked as seen.")
        return redirect(reverse("doctor_notifications"))


class DoctorProfileView(LoginRequiredMixin, CheckUserIsDoctorContextMixin, UpdateView):
    template_name = "doctor/profile.html"
    form_class = UpdateDoctorForm
    success_url = reverse_lazy("doctor_profile")

    def form_valid(self, form):
        # message success update doctor info
        messages.success(self.request, "Doctor profile updated successfully.")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Doctor, user=self.request.user)
