# Notes API (FastAPI, async, JWT, Postgres)

Небольшой сервис заметок: регистрация/логин по JWT, изолированный CRUD по заметкам, тесты и docker-compose для локального запуска.

---

## Стек
- FastAPI (async)
- SQLAlchemy 2.x (async) + PostgreSQL
- JWT для аутентификации, bcrypt для хеширования паролей
- Pytest (+ httpx, pytest-asyncio)
- Dockerfile + docker-compose

---

## Быстрый старт (Docker, рекомендовано)
```bash
# из корня проекта
cp .env.example .env
docker compose up --build -d

# проверка
docker compose ps
curl -s http://localhost:8000/docs >/dev/null && echo "API UP"
