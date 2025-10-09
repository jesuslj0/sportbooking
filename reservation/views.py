from django.shortcuts import render
from .models import Court

# Create your views here.
def courts_view(request):
    courts = Court.objects.all()
    context = {
        'courts': courts
    }
    return render(request, 'reservation/courts.html', context)

def court_detail_view(request, pk):
    court = Court.objects.get(pk=pk)
    context = {
        'court': court
    }
    return render(request, 'reservation/court_detail.html', context)