
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Reservation, Court, CourtSchedule
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CourtCreateForm, ScheduleCreateForm
from django import forms

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


@user_passes_test(is_manager)
def create_court_view(request, pk=None):
    if pk:
        court = get_object_or_404(Court, pk=pk)
        schedules = CourtSchedule.objects.filter(court=court).all().order_by('day_of_week', 'start_time')
    else:
        court = None
        schedules = None

    if request.method == 'POST':
        form = CourtCreateForm(request.POST, instance=court)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Pista guardada correctamente.')
                if court != None:
                    return redirect('reservas:admin_update_court', court.id)
                else:
                    return redirect('reservas:pistas')
            except Exception as e:
                messages.error(request, f'Error guardando la pista: {e}')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')

    else:
        form = CourtCreateForm(instance=court)
    context = {'form': form, 'court': court, 'schedules': schedules}
    return render(request, 'admin/court_form.html', context)

@user_passes_test(is_manager)
def create_schedule_view(request, pk=None, court_id=None):
    schedule = get_object_or_404(CourtSchedule, pk=pk) if pk else None
    court = None
    
    if court_id:
        court = get_object_or_404(Court, pk=court_id)

    if request.method == 'POST':
        form = ScheduleCreateForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule_obj = form.save(commit=False)

            if court_id and court:
                schedule_obj.court = court

            schedule_obj.save()
            messages.success(request, 'Horario guardado correctamente.')

            if court:
                return redirect('reservas:admin_update_court', court.id)
            return redirect('reservas:pistas')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        if court_id and court:
            form = ScheduleCreateForm(instance=schedule, initial={'court': court})
        else:
            form = ScheduleCreateForm(instance=schedule)
            
    context = {'form': form, 'schedule': schedule, 'court': court}
    return render(request, 'admin/schedule_form.html', context)


@user_passes_test(is_manager)
def delete_court_view(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == 'POST':
        try:
            court.delete()
            messages.success(request, 'Pista borrada correctamente.')
            return redirect('reservas:pistas')
        except Exception as e:
            messages.error(request, f'Error borrando la pista: {e}')
    context = {'court': court}
    return render(request, 'admin/court_confirm_delete.html', context)

@user_passes_test(is_manager)
def delete_schedule_view(request, pk):
    schedule = get_object_or_404(CourtSchedule, pk=pk)
    court_id = schedule.court.id
    if request.method == 'POST':
        try:
            schedule.delete()
            messages.success(request, 'Horario borrado correctamente.')
            return redirect('reservas:admin_update_court', pk=court_id)
        except Exception as e:
            messages.error(request, f'Error borrando el horario: {e}')
    context = {'schedule': schedule}
    return render(request, 'admin/schedule_confirm_delete.html', context)