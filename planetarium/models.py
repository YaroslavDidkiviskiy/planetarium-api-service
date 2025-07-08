import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify



class ShowTheme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def astronomy_show_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)

class AstronomyShow(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    theme = models.ManyToManyField(ShowTheme, related_name="astronomy_shows")
    image = models.ImageField(null=True, upload_to=astronomy_show_file_path)


    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name="show_sessions")
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE, related_name="show_sessions")
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show} о {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        if not (1 <= row <= planetarium_dome.rows):
            raise error_to_raise(
                {"row": f"Ряд має бути від 1 до {planetarium_dome.rows}"}
            )
        if not (1 <= seat <= planetarium_dome.seats_in_row):
            raise error_to_raise(
                {"seat": f"Місце має бути від 1 до {planetarium_dome.seats_in_row}"}
            )

    def clean(self):
        planetarium_dome = self.show_session.planetarium_dome
        self.validate_ticket(self.row, self.seat, planetarium_dome, ValidationError)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.show_session.planetarium_dome.name} (ряд: {self.row}, місце: {self.seat})"

    class Meta:
        unique_together = ("show_session", "row", "seat")
        ordering = ["row", "seat"]
