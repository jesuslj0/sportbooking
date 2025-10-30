from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reservation.models import Reservation, Court

@login_required(login_url='/users/login/')
def home_view(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).select_related('schedule__court').order_by('date')
    
    recurring_courts = (
        Court.objects
        .filter(schedules__reservation__user=user)
        .distinct()
        .order_by('schedules__reservation__date')
    )

    context = {
        'reservations': reservations,
        'recurring_courts': recurring_courts
    }

    return render(request, 'core/home.html', context)
