#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python create_superuser.py  # Make sure this file exists and works

echo "Collecting static files..."
python manage.py collectstatic --noinput

