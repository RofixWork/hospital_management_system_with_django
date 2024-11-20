from decimal import Decimal
from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from doctor.models import Doctor
from patient.models import Patient

from .forms import BookAppointmentForm
from .models import APPOINTMENT_TYPE, Appointment, Billing, BillingType, Service


# Create your views here.
class HomeView(ListView):
    model = Service
    template_name = "base/home.html"
    context_object_name = "services"


class ServiceDetailView(DetailView):
    model = Service
    template_name = "base/service_details.html"


class BookAppointmentView(LoginRequiredMixin, FormView):
    template_name = "base/book-appointment.html"
    form_class = BookAppointmentForm
    success_url = reverse_lazy("home")

    def validate_request(self):
        service_id = self.kwargs.get("service_id")
        doctor_id = self.kwargs.get("doctor_id")
        self.service = get_object_or_404(Service, id=service_id)
        self.doctor = get_object_or_404(Doctor, id=doctor_id)
        self.patient = get_object_or_404(Patient, user=self.request.user)
        if not self.service.doctors_available.filter(id=self.doctor.id).exists():
            raise Http404

    def dispatch(self, request, *args, **kwargs):
        try:
            self.validate_request()
        except (
            Http404,
            Service.DoesNotExist,
            Patient.DoesNotExist,
            Doctor.DoesNotExist,
        ):
            return redirect(
                reverse("service_details", kwargs={"pk": self.kwargs.get("service_id")})
            )
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["doctor"] = self.doctor
        form = self.form_class(
            initial={
                "full_name": self.patient.full_name,
                "email": self.patient.email,
                "mobile": self.patient.mobile,
                "gender": self.patient.gender,
                "date_of_birth": self.patient.date_of_birth,
                "address": self.patient.address,
            }
        )
        context["form"] = form
        return context

    def form_valid(self, form: BookAppointmentForm):
        # update patient
        self.patient.full_name = form.cleaned_data.get("full_name")
        self.patient.email = form.cleaned_data.get("email")
        self.patient.mobile = form.cleaned_data.get("mobile")
        self.patient.gender = form.cleaned_data.get("gender")
        self.patient.date_of_birth = form.cleaned_data.get("date_of_birth")
        self.patient.address = form.cleaned_data.get("address")
        self.patient.save()

        # create appointment
        issues = form.cleaned_data.get("issues")
        symptoms = form.cleaned_data.get("symptoms")
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            service=self.service,
            issues=issues,
            symptoms=symptoms,
            status=APPOINTMENT_TYPE.SCHEDULED,
        )

        # create a new billing
        billing = Billing()
        billing.appointment = appointment
        billing.patient = self.patient
        billing.status = BillingType.UNPAID
        billing.sub_total = appointment.service.cost
        billing.tax = billing.sub_total * Decimal("0.05")
        billing.total = billing.sub_total + billing.tax
        billing.save()

        return redirect(
            reverse(
                "checkout",
                kwargs={
                    "appointment_id": appointment.appointment_id,
                    "billing_id": billing.billing_id,
                },
            )
        )


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "base/checkout.html"

    def dispatch(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get("appointment_id")
        billing_id = self.kwargs.get("billing_id")
        self.patient = get_object_or_404(Patient, user=request.user)
        self.appointment = get_object_or_404(
            Appointment, appointment_id=appointment_id, patient=self.patient
        )
        self.billing = get_object_or_404(
            Billing, billing_id=billing_id, patient=self.patient
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"] = self.patient
        context["doctor"] = self.appointment.doctor
        context["billing"] = self.billing
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        return context
