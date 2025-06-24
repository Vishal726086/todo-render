import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoproject.settings")
django.setup()

User = get_user_model()
if not User.objects.filter(username="vishal").exists():
    User.objects.create_superuser("vishal", "alphaz010101@gmail.com", "todoapp11")
