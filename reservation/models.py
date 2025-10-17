from django.db import models
from django.contrib.auth.models import User


class Court(models.Model):
    TYPE_CHOICES = [
        ("football", "Fútbol"),
        ("tennis", "Tenis"),
        ("padel", "Pádel"),
        ("basket", "Baloncesto"),
        ("racquetball", "Frontenis"),
        ("waterpool", "Piscina")
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    class Meta:
        verbose_name = "Pista"
        verbose_name_plural = "Pistas"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("confirmed", "Confirmada"),
        ("cancelled", "Cancelada"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        unique_together = ("court", "date", "start_time", "end_time")  # evita solapamientos exactos
        ordering = ["-date", "start_time"]

    def __str__(self):
        return f"{self.court} - {self.date} {self.start_time}-{self.end_time}"

class CourtSchedule(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(
        choices=[
            (0, "Lunes"),
            (1, "Martes"),
            (2, "Miércoles"),
            (3, "Jueves"),
            (4, "Viernes"),
            (5, "Sábado"),
            (6, "Domingo"),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "Horario de Pista"
        verbose_name_plural = "Horarios de Pistas"
        unique_together = ("court", "day_of_week", "start_time", "end_time")
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.court} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"