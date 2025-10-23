from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reservation.models import Reservation

@login_required(login_url='/users/login/')
def home_view(request):
    user = request.user
    reservations = Reservation.objects.filter(user_id=user.id).order_by('date')
    return render(request, 'core/home.html', {'reservations': reservations})
