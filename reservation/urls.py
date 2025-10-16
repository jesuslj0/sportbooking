from django.urls import path
from . import views

app_name = 'reservas'
urlpatterns = [
    path('pistas/', views.courts_view, name='pistas'),
    path('pistas/<int:pk>/', views.court_detail_view, name='pista')
]