from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ["sportbooking-fkkb.onrender.com", "www.sportbooking-fkkb.onrender.com"]
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

