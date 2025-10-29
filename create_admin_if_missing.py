import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Solo crea el admin si no existe
username = "admin"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="admin@example.com",
        password="URZWhGAS"
    )
    print(f"Superuser {username} creado.")
else:
    print("Superuser ya existe, no se crea.")
