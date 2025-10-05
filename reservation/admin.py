from django.contrib import admin
from .models import Court, Reservation

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
