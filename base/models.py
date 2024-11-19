import shortuuid
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from doctor.models import Doctor
from patient.models import Patient


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    thumbnail = models.ImageField(upload_to="images")
    doctors_available = models.ManyToManyField(Doctor)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Services"
        verbose_name = "Service"

    def __str__(self):
        return f"{self.name} (${self.cost:.2f})"

    @property
    def tax(self) -> float:
        return max(0, self.cost * 0.05)


class Appointment(models.Model):

    class APPOINTMENT_TYPE(models.TextChoices):
        PENDING = "pending", "Pending"
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor_appointments",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_appointments",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_appointments",
    )
    appointment_id = shortuuid.ShortUUID(alphabet="1234567890").random(length=6)
    appointment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPE.choices,
        default=APPOINTMENT_TYPE.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Appointments"
        verbose_name = "Appointment"

    def __str__(self) -> str:
        patient_name = getattr(self.patient, "full_name", "Unknown Patient")
        doctor_name = getattr(self.doctor, "full_name", "Unknown Doctor")
        return f"Appointment for {patient_name} with Dr. {doctor_name}"


class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Medical Records"
        verbose_name = "Medical Record"

    def __str__(self) -> str:
        return f"Medical Record for {getattr(self.appointment.patient, 'full_name', 'Unknown')}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    description = models.TextField()
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "LabTest"
        verbose_name_plural = "LabTests"

    def __str__(self) -> str:
        return f"{self.test_name} for {getattr(self.appointment.patient, 'full_name', 'Unknown')}"


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

    def __str__(self) -> str:
        return f"Prescription for {getattr(self.appointment.patient, 'full_name', 'Unknown')}"
