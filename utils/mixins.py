from typing import Any

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class RedirectAuthenticationUser:
    """
    Custom authentication backend for redirecting authenticated users to a specific URL
    """

    redirect_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                self.redirect_url
            )  # Redirect authenticated users to the home page
        return super().dispatch(request, *args, **kwargs)


class CheckUserIsADoctorDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "doctor"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.doctor = request.user.doctor
        return super().dispatch(request, *args, **kwargs)


class CheckUserIsDoctorContextMixin(CheckUserIsADoctorDispatchMixin):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["doctor"] = self.doctor
        return context


class CheckUserIsPatientContextMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "patient"):
            logout(request)
            return redirect(reverse("auth.login"))

        self.patient = request.user.patient
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["patient"] = self.patient
        return context
