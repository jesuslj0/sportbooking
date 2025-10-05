from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from users.views import login_view, register_view, logout_view

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('reservation/', include('reservation.urls', 'reservation'))
]