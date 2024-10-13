#!/bin/sh

if [ "$(python manage.py showmigrations | grep '\[ ]' | wc -l)" -gt 0 ]; then
    echo "Running makemigrations..."
    python manage.py makemigrations
fi

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
