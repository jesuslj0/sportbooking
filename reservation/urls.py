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

    path('reserva/<int:pk>/anular', users_views.cancel_reservation_view, name='cancel_reservation')
]