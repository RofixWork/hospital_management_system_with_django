from django.db import models

from userauths.models import User
from utils.custom_validations import CustomValidations


# Create your models here.
class NotificationType(models.TextChoices):
    SCHEDULED_APPOINTMENT = "scheduled appointment", "Scheduled Appointment"
    CANCELLED_APPOINTMENT = "cancelled appointment", "Cancelled Appointment"


class GENDER_TYPE(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    blood_group = models.CharField(max_length=40, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=50, blank=True, null=True, choices=GENDER_TYPE.choices
    )
    image = models.ImageField(upload_to="images", blank=True, null=True)
    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        validators=[CustomValidations.check_phone_number],
    )

    def __str__(self):
        return self.full_name if self.full_name else "Unamed Patient"


class Notification(models.Model):
    appointment = models.ForeignKey(
        "base.Appointment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_appointment_notifications",
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    type = models.CharField(
        max_length=30, choices=NotificationType.choices, blank=True, null=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return (
            f"Notification for {getattr(self.patient, 'full_name', 'Unamed Patient')}"
        )
