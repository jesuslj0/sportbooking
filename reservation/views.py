from django.shortcuts import render
from .models import Court

# Create your views here.
def courts_view(request):
    courts = Court.objects.all()
    context = {
        'courts': courts
    }
    return render(request, 'reservation/courts.html', context)