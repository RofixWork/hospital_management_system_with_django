from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.TextChoices):
    PATIENT = "patient", "Patient"
    Doctor = "doctor", "Doctor"


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=60, blank=True, null=True)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "user_type"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            email_username, _ = self.email.split("@")
            self.username = email_username.lower()
        return super().save(*args, **kwargs)
