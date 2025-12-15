# Liquidpedia API

Короткий опис:  
Бекенд для роботи з аналогом вікіпедії для спорту та кіберспорту

## Члени команди
- **Ілля** – розробка створення та оновлення замовлень, аналітичні запити, інтеграційні тести, налаштування Docker, документація  +- все

## Технологічний стек
- **Мова програмування:** Python
- **ORM / SQL builder:** Django ORM
- **Фреймворк тестування:** rest_framework.test
- **Система контейнеризації:** Docker, docker-compose  
- **База даних:** PostgreSQL  

## Інструкції з налаштування

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/your-repo/project.git
   cd project

    Запустіть сервіси:

    docker-compose up --build
    docker-compose up -d

Запуск додатку

    docker-compose up -d

Запуск тестів

    Запустити всі тести:

        docker-compose run --rm test python manage.py migrate

Запустити конкретний тестовий файл:

    docker-compose run --rm test python manage.py test myapp.tests.test_olap_api
    docker-compose run --rm test python manage.py test myapp.tests.tests

Огляд структури проєкту


    backend/
    ├─ core/                     # Основные настройки проекта
    │  ├─ __init__.py
    │  ├─ asgi.py
    │  ├─ settings.py
    │  ├─ urls.py
    │  └─ wsgi.py
    ├─ myapp/                     # Основное приложение
    │  ├─ __init__.py
    │  ├─ admin.py
    │  ├─ apps.py
    │  ├─ models.py              # Team, Roster, Player
    │  ├─ serializers.py
    │  ├─ urls.py                # API endpoints
    │  ├─ views.py
    │  ├─ team/                  # Логика команды (сервисы, utils)
    │  │  ├─ __init__.py
    │  │  └─ service.py
    │  │  └─ player_analytics.py
    │  └─ tests/                 # Тесты
    │     ├─ __init__.py
    │     ├─ test_olap_api.py
    │     └─ test_team_api.py
    ├─ manage.py
    ├─ Dockerfile
    ├─ entrypoint.sh
    ├─ requirements.txt
    ├─ docker-compose.yml
    └─ docs/

### Приклади API / використання

    Створити комунду:

    POST /create-team/
    {
            "team_name": "Test Team Alpha",
            "roster_start_date": "2025-01-01",
            "players": [{"nick": "P1", "age": 25}]
    }

Оновлення команди:

    POST /update-team/
    {
        "team_id": 1,
        "new_team_name": "New Team Name"
    }

Видалення команди:

    DELETE /delete-team/id
    result:
    {
    "success": true,
    "team_id": 2
    }

    DELETE /soft-delete-player/id
    result:
    {
    "success": true,
    "player_id": 1
}

### Аналітика

Гравці за віком

    GET /players-by-age/
    result:
     {
        "id": 4,
        "nick": "ATest",
        "age": 19,
        "team_id": 2,
        "team_name": "Mandalorec"
    },
    {
        "id": 5,
        "nick": "Btest",
        "age": 20,
        "team_id": 2,
        "team_name": "Mandalorec"
    },
    {
        "id": 6,
        "nick": "AbTest",
        "age": 21,
        "team_id": 2,
        "team_name": "Mandalorec"
    },
    {
        "id": 7,
        "nick": "P1",
        "age": 25,
        "team_id": 3,
        "team_name": "New Team Name"
    }

Гравці за абеткою

    GET /players-by-abc/
    result: 
    {
        "id": 6,
        "nick": "AbTest",
        "age": 21,
        "team_id": 2,
        "team_name": "Mandalorec"
    },
    {
        "id": 4,
        "nick": "ATest",
        "age": 19,
        "team_id": 2,
        "team_name": "Mandalorec"
    },
    {
        "id": 5,
        "nick": "Btest",
        "age": 20,
        "team_id": 2,
        "team_name": "Mandalorec"
    },
    {
        "id": 7,
        "nick": "P1",
        "age": 25,
        "team_id": 3,
        "team_name": "New Team Name"
    }



GitHub репозиторій:https://github.com/ilyabukhantsov/bd-labs/tree/main/course-work