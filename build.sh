#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python create_superuser.py  # Make sure this file exists and works

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "from django.contrib.auth import get_user_model; User = get_user_model(); u=User.objects.get(username='vishal'); u.is_staff=True; u.is_superuser=True; u.save()" | python manage.py shell

