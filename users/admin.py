from django.contrib import admin

# Register your models here.
from .models import User

@admin.register(User)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_manager', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('date_joined',)
