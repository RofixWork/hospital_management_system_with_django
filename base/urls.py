from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("service/<int:pk>", views.ServiceDetailView.as_view(), name="service_details"),
    path(
        "book-appointment/<int:service_id>/<int:doctor_id>/",
        views.BookAppointmentView.as_view(),
        name="book_appointment",
    ),
    path(
        "checkout/<billing_id>",
        views.CheckoutView.as_view(),
        name="checkout",
    ),
    path(
        "stripe_payment/<billing_id>/",
        csrf_exempt(views.StripePaymentView.as_view()),
        name="stripe_payment",
    ),
    path(
        "stripe-payment-verify/<billing_id>/",
        views.PaymentStripeVerifyView.as_view(),
        name="stripe_payment_verify",
    ),
    path(
        "payment-status/<billing_id>",
        views.PaymentStatusView.as_view(),
        name="payment_status",
    ),
]
