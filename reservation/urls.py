from django.urls import path
from . import users_views
from . import admin_views

app_name = 'reservas'
urlpatterns = [
    path('pistas/', users_views.courts_view, name='pistas'),
    path('pistas/<int:pk>/', users_views.court_detail_view, name='pista'),
    path('reservar/<int:pk>/', users_views.book_court_view, name='reservar'),
    path('schedules/<int:court_id>/<int:day_id>', users_views.get_schedules_by_day, name='get_schedules_by_day'),
    
    path('admin/dashboard', admin_views.dashboard, name='admin_dashboard' ),
    path('admin/reserva/<int:pk>/confirmar', admin_views.confirm_reservation, name='confirm_reservation'),
    path('admin/reserva/<int:pk>/cancelar', admin_views.cancel_reservation, name='admin_cancel_reservation'),
    path('admin/nueva_pista', admin_views.create_court_view, name='admin_create_court'),
    path('admin/nuevo_horario', admin_views.create_schedule_view, name='admin_create_schedule'),
    path('admin/nuevo_horario/<int:court_id>', admin_views.create_schedule_view, name='admin_create_schedule'),
    path('admin/editar_pista/<int:pk>', admin_views.create_court_view, name='admin_update_court'),
    path('admin/editar_horario/<int:pk>', admin_views.create_schedule_view, name='admin_update_schedule'),
    path('admin/borrar_pista/<int:pk>', admin_views.delete_court_view, name='admin_delete_court'),
    path('admin/borrar_horario<int:pk>', admin_views.delete_schedule_view, name='admin_delete_schedule'),

    path('reserva/<int:pk>/anular', users_views.cancel_reservation_view, name='cancel_reservation')
]