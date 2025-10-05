from django.urls import path
from . import views

app_name = 'reservation'
urlpatterns = [
    path('pistas/', views.courts_view, name='pistas'),
]