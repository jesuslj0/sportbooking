from django.urls import path
from . import views

app_name = 'reservas'
urlpatterns = [
    path('pistas/', views.courts_view, name='pistas'),
    path('pistas/<int:pk>/', views.court_detail_view, name='pista'),
    path('reservar/<int:pk>/', views.book_court_view, name='reservar'),
    path('schedules/<int:court_id>/<int:day_id>', views.get_schedules_by_day, name='get_schedules_by_day'),
]