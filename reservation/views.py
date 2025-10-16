from django.shortcuts import render
from .models import Court, Reservation

# Create your views here.
def courts_view(request):
    courts = Court.objects.all().order_by('type')
    context = {
        'courts': courts
    }
    return render(request, 'reservation/courts.html', context)

def court_detail_view(request, pk):
    court = Court.objects.get(pk=pk)
    reservations = Reservation.objects.filter(court = court)

    context = {
        'court': court,
        'reservations': reservations
    }
    return render(request, 'reservation/court_detail.html', context)