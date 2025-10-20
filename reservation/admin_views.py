
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation, Court
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def is_manager(user):
    return user.is_authenticated and user.is_manager

@user_passes_test(is_manager)
def dashboard(request):
    reservations = Reservation.objects.all().order_by('date', 'schedule__start_time')
    courts = Court.objects.all()

    date = request.GET.get('date')
    status = request.GET.get('status')
    court = request.GET.get('court')

    if date:
        reservations = reservations.filter(date=date)
    if status:
        reservations = reservations.filter(status=status)
    if court:
        reservations = reservations.filter(schedule__court_id=court)

    context = {
        'reservations': reservations,
        'courts': courts
    }

    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_manager)
def confirm_reservation(request, pk):
    reserva = get_object_or_404(Reservation, pk=pk)
    resultado = reserva.confirm()
    
    if resultado == 'ok':
        messages.success(request, 'Reserva confirmada correctamente.')
    elif resultado == 'cancelled':
        messages.warning(request, 'No se puede confirmar: la reserva está cancelada.')
    elif resultado == 'other_confirmed':
        messages.warning(request, 'No se puede confirmar: ya existe otra reserva confirmada igual.')

    return redirect('reservas:admin_dashboard')

@user_passes_test(is_manager)
def cancel_reservation(request, pk):
    reserva = get_object_or_404(Reservation, pk=pk)
    reserva.cancell()
    return redirect('reservas:admin_dashboard')