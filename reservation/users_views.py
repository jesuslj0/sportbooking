from django.shortcuts import render, redirect
from .models import Court, Reservation, CourtSchedule
from datetime import time, timedelta, datetime
from .forms import BookForm
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def courts_view(request):
    courts = Court.objects.all().order_by('type')
    context = {
        'courts': courts
    }
    return render(request, 'reservation/courts.html', context)

def court_detail_view(request, pk):
    court = Court.objects.get(pk=pk)
    reservations = Reservation.objects.filter(schedule__court_id = pk).order_by('date')
    schedules = CourtSchedule.objects.filter(court_id = pk).order_by('day_of_week', 'start_time')

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

def book_court_view(request, pk):
    court = Court.objects.get(pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, court=court)
        if form.is_valid():
            booking = Reservation(
                user=request.user,
                schedule=form.cleaned_data['schedule_instance'],
                date=form.cleaned_data['date']
            )
            booking.save()
            messages.success(request, 'Reserva creada exitosamente!')
            return redirect('reservas:pista', pk=court.pk)
    else:
        form = BookForm(court=court)

    context = {
        'court': court,
        'form': form
    }

    return render(request, 'reservation/book_court.html', context)



def get_schedules_by_day(request, court_id, day_id):
    schedules = CourtSchedule.objects.filter(
        court_id=court_id, day_of_week=day_id
    ).order_by("start_time")

    data = [
        {"id": s.pk, "text": f"{s.start_time:%H:%M} - {s.end_time:%H:%M}"}
        for s in schedules
    ]
    return JsonResponse(data, safe=False)

def cancel_reservation_view(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk, user=request.user)
        reservation.delete()
        messages.success(request, 'Reserva anulada exitosamente.')
    except Reservation.DoesNotExist:
        messages.error(request, 'No se encontró la reserva o no tienes permiso para cancelarla.')
    return redirect('home')