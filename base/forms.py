from django import forms
from django.core import validators

from patient.models import GENDER_TYPE
from utils.custom_validations import CustomValidations


class BookAppointmentForm(forms.Form):
    full_name = forms.CharField(
        max_length=60,
        validators=[
            validators.MinLengthValidator(6),
            validators.RegexValidator(
                regex=r"^[A-Za-z]+\s[A-Za-z]+$",
                message="Please enter a valid full name with a first and last name, separated by a space (e.g., John Doe).",
            ),
        ],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Jhon Doe"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "jhondoe@gmail.com"}
        )
    )

    mobile = forms.CharField(
        max_length=40,
        validators=[CustomValidations.check_phone_number],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+1 123-456-7890"}
        ),
    )

    gender = forms.ChoiceField(
        choices=GENDER_TYPE.choices, widget=forms.Select(attrs={"class": "form-select"})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "123 Main St"}
        ),
    )
    issues = forms.CharField(
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Any specific medical issues or concerns",
            }
        ),
    )
    symptoms = forms.CharField(
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Describe the symptoms you're experiencing",
            }
        ),
    )
