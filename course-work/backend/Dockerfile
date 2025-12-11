FROM python:3.12

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Делаем entrypoint исполняемым
RUN chmod +x /app/entrypoint.sh

# Запуск entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
