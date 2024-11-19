from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Service


# Create your views here.
class HomeView(ListView):
    model = Service
    template_name = "base/home.html"
    context_object_name = "services"


class ServiceDetailView(DetailView):
    model = Service
    template_name = "base/service_details.html"
