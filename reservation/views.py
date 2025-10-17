from django.shortcuts import render
from .models import Court, Reservation, CourtSchedule
from datetime import time, timedelta, datetime

# Create your views here.
def courts_view(request):
    courts = Court.objects.all().order_by('type')
    context = {
        'courts': courts
    }
    return render(request, 'reservation/courts.html', context)

def court_detail_view(request, pk):
    court = Court.objects.get(pk=pk)
    reservations = Reservation.objects.filter(court = court).order_by('date')
    schedules = CourtSchedule.objects.filter(court = court).order_by('day_of_week', 'start_time')

    days = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    grouped = {d[0]: [] for d in days}
    for s in schedules:
        grouped[s.day_of_week].append(s)

    context = {
        'court': court,
        'reservations': reservations,
        'grouped': grouped,
        'days': days,
    }
    return render(request, 'reservation/court_detail.html', context)