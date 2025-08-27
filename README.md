# Notes API

Небольшой сервис заметок: регистрация/логин по JWT, изолированный CRUD по заметкам, тесты и docker-compose для локального запуска.

## Быстрый старт
```bash
# из корня проекта
cp .env.example .env
docker compose up --build -d

# проверка
docker compose ps
curl -s http://localhost:8000/docs >/dev/null && echo "API UP"
