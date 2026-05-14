# departmentAPI


## Развёртывание в системе

python3 -m venv venv создание виртуального окружения
source venv/bin/activate активация виртуального окружения
pip install -r requirements.txt установка зависимостей

## Docker

docker-compose up -d запуск контейнеров в фоне

## Как задезть вовнутрь БД в докере (подзказка для себя)

psql -h localhost -U postgres -d postgres