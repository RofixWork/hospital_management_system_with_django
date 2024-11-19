from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("service/<int:pk>", views.ServiceDetailView.as_view(), name="service_details"),
]
