#!/bin/sh

# Migrations'larni ko'rsatish va agar bo'sh migrations bo'lsa, yangilarini yaratish
if [ "$(python manage.py showmigrations | grep '\[ ]' | wc -l)" -gt 0 ]; then
    echo "Running makemigrations..."
    python manage.py makemigrations
fi

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Django runserver o'rniga gunicorn serverdan foydalanish
echo "Starting Gunicorn server..."
exec gunicorn book_audio.wsgi:application --bind 0.0.0.0:8000 --workers 3
