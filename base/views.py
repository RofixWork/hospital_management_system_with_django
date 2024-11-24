from decimal import Decimal
from typing import Any

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    Http404,
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from doctor.models import Doctor
from doctor.models import Notification as DoctorNotification
from doctor.models import NotificationType as DoctorNotificationType
from patient.models import Notification as PatientNotification
from patient.models import NotificationType as PatientNotificationType
from patient.models import Patient
from utils.mixins import CheckUserIsPatientContextMixin

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
        if not self.request.user.is_authenticated:
            raise Http404
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
                    "billing_id": billing.billing_id,
                },
            )
        )


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "base/checkout.html"

    def dispatch(self, request, *args, **kwargs):
        billing_id = self.kwargs.get("billing_id")
        self.patient = get_object_or_404(Patient, user=request.user)
        self.billing = get_object_or_404(
            Billing,
            billing_id=billing_id,
            patient=self.patient,
        )
        self.appointment = get_object_or_404(
            Appointment,
            appointment_id=self.billing.appointment.appointment_id,
            patient=self.patient,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"] = self.patient
        context["doctor"] = self.appointment.doctor
        context["billing"] = self.billing
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        return context


class StripePaymentView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        billing_id = self.kwargs.get("billing_id")
        self.patient = get_object_or_404(Patient, user=request.user)
        self.billing = get_object_or_404(Billing, billing_id=billing_id)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=self.billing.patient.email,
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": self.billing.appointment.service.name,
                            },
                            "unit_amount": int(self.billing.total * 100),
                        },
                        "quantity": 1,
                    }
                ],
                success_url=request.build_absolute_uri(
                    reverse(
                        "stripe_payment_verify",
                        kwargs={"billing_id": self.billing.billing_id},
                    )
                )
                + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(
                    reverse(
                        "stripe_payment_verify",
                        kwargs={"billing_id": self.billing.billing_id},
                    )
                ),
            )
            return JsonResponse({"sessionId": session.id})
        except stripe.error.StripeError as e:
            return JsonResponse({"error": "Invalid Session Id"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class PaymentStripeVerifyView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        billing_id = self.kwargs.get("billing_id")
        self.patient = get_object_or_404(Patient, user=request.user)
        self.billing = get_object_or_404(Billing, billing_id=billing_id)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        sessionId = self.request.GET.get("session_id")
        if sessionId:
            try:
                session = stripe.checkout.Session.retrieve(sessionId)

                if session.payment_status == "paid":
                    if self.billing.status == BillingType.UNPAID:
                        self.billing.status = BillingType.PAID
                        self.billing.save()

                        PatientNotification.objects.create(
                            appointment=self.billing.appointment,
                            patient=self.billing.appointment.patient,
                            type=PatientNotificationType.SCHEDULED_APPOINTMENT,
                        )

                        DoctorNotification.objects.create(
                            appointment=self.billing.appointment,
                            doctor=self.billing.appointment.doctor,
                            type=DoctorNotificationType.NEW_APPOINTMENT,
                        )
                        return redirect(
                            f"{reverse('payment_status', kwargs={
                            'billing_id': self.billing.billing_id
                        })}?status=success"
                        )

            except (stripe.error.InvalidRequestError, Exception):
                return redirect(
                    f"{reverse('payment_status', kwargs={
                    'billing_id': self.billing.billing_id
                })}?status=failed"
                )
            except Exception as e:
                return HttpResponseServerError("An error occurred: " + str(e))


class PaymentStatusView(LoginRequiredMixin, DetailView):
    template_name = "base/payment_status.html"
    model = Billing

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["status"] = self.request.GET.get("status")
        return context

    def get_object(self, queryset=None):
        billing_id = self.kwargs.get("billing_id")
        patient = get_object_or_404(Patient, user=self.request.user)
        return get_object_or_404(Billing, billing_id=billing_id, patient=patient)
