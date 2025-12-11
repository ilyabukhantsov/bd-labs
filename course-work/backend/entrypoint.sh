#!/bin/bash
set -e

# Перейти в рабочую директорию
cd /app

# Если manage.py нет — создаём проект Django
if [ ! -f "manage.py" ]; then
    echo "Creating Django project..."
    django-admin startproject core .
fi

# Применяем миграции
python manage.py migrate --noinput

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000
