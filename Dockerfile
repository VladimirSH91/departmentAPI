FROM python:3.10-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY src/ ./src/

# Копирование entrypoint скрипта
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Создание директории для миграций если нужно
RUN mkdir -p src/app/migration/versions

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src/app

# Запуск приложения через entrypoint
CMD ["./entrypoint.sh"]
