from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("sign-up/", views.RegisterView.as_view(), name="auth.register"),
    path("sign-in/", views.LoginView.as_view(), name="auth.login"),
    path("sign-out/", LogoutView.as_view(), name="auth.logout"),
]
