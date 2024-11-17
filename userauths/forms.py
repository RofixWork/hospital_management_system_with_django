from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

from userauths.models import User, UserType


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Jhon Doe"}
        ),
        validators=[
            validators.MinLengthValidator(6),
            validators.RegexValidator(
                regex=r"^[A-Za-z]+\s[A-Za-z]+$",
                message="Please enter a valid full name with a first and last name, separated by a space (e.g., John Doe).",
            ),
        ],
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "jhondoe@gmail.com"}
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "***********"}
        ),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "***********"}
        ),
    )
    user_type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select"}), choices=UserType.choices
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "user_type"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "jhondoe@gmail.com"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "***********"}
        )
    )
