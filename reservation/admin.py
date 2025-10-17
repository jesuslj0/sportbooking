from django.contrib import admin
from .models import Court, Reservation, CourtSchedule

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "location")
    list_filter = ("type",)
    search_fields = ("name", "location")
    verbose_name = "Pista"
    verbose_name_plural = "Pistas"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("court", "user", "date", "start_time", "end_time", "status")
    list_filter = ("status", "date", "court")
    search_fields = ("user__username", "court__name")
    ordering = ("-date", "start_time")
    verbose_name = "Reserva"
    verbose_name_plural = "Reservas"

@admin.register(CourtSchedule)
class CourtScheduleAdmin(admin.ModelAdmin):
    list_display = ("court", "day_of_week", "start_time", "end_time")
    list_filter = ("day_of_week", "court")
    search_fields = ("court__name",)
    ordering = ("day_of_week", "start_time")
    verbose_name = "Horario de Pista"
    verbose_name_plural = "Horarios de Pista"