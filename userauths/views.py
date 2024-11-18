from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from doctor.models import Doctor
from patient.models import Patient
from userauths.models import User
from utils.mixins import RedirectAuthenticationUser

from .forms import UserLoginForm, UserRegisterForm


# Create your views here.
class RegisterView(RedirectAuthenticationUser, CreateView):
    model = User
    template_name = "userauths/sign-up.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("auth.login")

    def form_valid(self, form: UserRegisterForm):
        user = form.save()
        full_name = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        user_type = form.cleaned_data.get("user_type")

        if user_type == "doctor":
            Doctor.objects.create(user=user, full_name=full_name)
        elif user_type == "patient":
            Patient.objects.create(user=user, full_name=full_name, email=email)
        return super().form_valid(form)


class LoginView(RedirectAuthenticationUser, FormView):
    template_name = "userauths/sign-in.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: UserLoginForm):
        # Process the form data here.
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # Authenticate the user using the provided email and password.
        # You can use Django's built-in authentication system or implement your own.
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)  # Log the user in.
            return super().form_valid(form)
        else:
            form.add_error(None, "Authentication Failed, please try Again...")
            return super().form_invalid(form)
