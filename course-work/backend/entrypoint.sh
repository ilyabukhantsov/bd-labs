#!/bin/bash
set -e

cd /app

if [ ! -f "manage.py" ]; then
    echo "Creating Django project (Skipping in production/test context usually)..."
    django-admin startproject core .
fi

python manage.py migrate --noinput


if [ "$#" -gt 0 ]; then
    echo "Executing command: $@"
    exec "$@"
else
    echo "No command provided. Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
fi