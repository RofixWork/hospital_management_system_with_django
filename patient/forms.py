from django import forms

from .models import Patient


class UpdatePatientForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Patient
        fields = [
            "image",
            "full_name",
            "email",
            "mobile",
            "gender",
            "date_of_birth",
            "blood_group",
            "address",
        ]
        labels = {
            "image": "Profile Avatar",
        }
        widgets = {
            "image": forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control"}),
            "blood_group": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["email"].initial = self.instance.user.email
