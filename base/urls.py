from django.urls import path

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
        "checkout/<appointment_id>/<billing_id>",
        views.CheckoutView.as_view(),
        name="checkout",
    ),
]
