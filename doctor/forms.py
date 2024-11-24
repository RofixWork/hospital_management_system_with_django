from django import forms

from .models import Doctor


class UpdateDoctorForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Doctor
        fields = [
            "image",
            "full_name",
            "email",
            "mobile",
            "bio",
            "country",
            "specializations",
            "qualifications",
            "years_of_experience",
            "next_available_appointment_date",
        ]
        labels = {
            "image": "Profile Avatar",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "specializations": forms.Textarea(attrs={"class": "form-control"}),
            "qualifications": forms.Textarea(attrs={"class": "form-control"}),
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control"}),
            "next_available_appointment_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "image": forms.widgets.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["email"].initial = self.instance.user.email
