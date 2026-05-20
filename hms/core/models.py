from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    google_credentials = models.JSONField(
        null=True,
        blank=True
    )

    def __str__(self):

        return self.username


class Slot(models.Model):

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='slots'
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    is_booked = models.BooleanField(
        default=False
    )

    def __str__(self):

        return f"{self.doctor.username} | {self.start_time}"


class Booking(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('confirmed', 'Confirmed'),

        ('completed', 'Completed'),

        ('cancelled', 'Cancelled'),

    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    calendar_event_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.patient.username} booked {self.slot}"


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:40]}"