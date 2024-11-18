from django.db import models

from userauths.models import User
from utils.custom_validations import CustomValidations


class NotificationType(models.TextChoices):
    NEW_APPOINTMENT = "new appointment", "New Appointment"
    CANCELLED_APPOINTMENT = "cancelled appointment", "Cancelled Appointment"


# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=400, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    mobile = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        unique=True,
        validators=[CustomValidations.check_phone_number],
    )
    next_available_appointment_date = models.DateTimeField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    specializations = models.TextField(null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name if f"Dr. {self.full_name}" else "Unamed Doctor"


class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    type = models.CharField(
        max_length=30, choices=NotificationType.choices, blank=True, null=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return (
            f"Notification for {getattr(self.doctor, 'full_name',  'Unknown Doctor')}"
        )
