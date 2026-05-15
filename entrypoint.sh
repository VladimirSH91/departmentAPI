#!/bin/bash
set -e

# Ждём пока PostgreSQL будет доступен
echo "Waiting for PostgreSQL..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Запуск миграций
echo "Running database migrations..."
cd /app/src/app
alembic upgrade head
echo "Migrations completed!"

# Запуск приложения
echo "Starting application..."
cd /app
python -m uvicorn main:app --host 0.0.0.0 --port 8000
