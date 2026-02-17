# 🚀 Quick Start - Phil Backend

## Самый быстрый способ запустить проект

### Вариант 1: Автоматический запуск (Рекомендуется)

```bash
cd phil-backend
./start.sh
```

Скрипт автоматически:
- ✅ Создаст .env файл
- ✅ Соберёт Docker контейнеры
- ✅ Запустит все сервисы
- ✅ Применит миграции БД
- ✅ Соберёт статические файлы

### Вариант 2: Ручной запуск

```bash
cd phil-backend

# 1. Создать .env файл
cp .env.example .env

# 2. Запустить Docker Compose
docker-compose up --build -d

# 3. Дождаться запуска сервисов (10-15 секунд)
docker-compose logs -f backend

# 4. Применить миграции
docker-compose exec backend python manage.py migrate

# 5. Собрать статику
docker-compose exec backend python manage.py collectstatic --noinput
```

### Вариант 3: С использованием Make

```bash
cd phil-backend

# Создать .env
cp .env.example .env

# Собрать и запустить
make build
make up

# Применить миграции
make migrate
```

## После запуска

### 1. Создайте суперпользователя

```bash
docker-compose exec backend python manage.py createsuperuser
```

Введите:
- Username: `admin`
- Email: `admin@example.com`
- Password: (ваш пароль)

### 2. Откройте API

- **API Root:** http://localhost:8000/api/
- **Links API:** http://localhost:8000/api/links/
- **Stats API:** http://localhost:8000/api/stats/dashboard/
- **Admin Panel:** http://localhost:8000/admin/

### 3. Протестируйте API

```bash
# Автоматический тест всех endpoints
./test_api.sh

# Или вручную
curl http://localhost:8000/api/links/
```

## Что дальше?

### Посмотреть логи
```bash
docker-compose logs -f backend
```

### Остановить сервисы
```bash
docker-compose down
```

### Перезапустить сервисы
```bash
docker-compose restart
```

### Очистить всё (включая БД)
```bash
docker-compose down -v
```

## Интеграция с Frontend

В вашем Next.js проекте установите:

```env
# frontend/.env.local
NEXT_PUBLIC_USE_MOCK=false
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Готово! Frontend может теперь обращаться к backend API.

## Быстрые тесты

### Создать тестовую ссылку
```bash
curl -X POST http://localhost:8000/api/links/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://facebook.com/test-post",
    "platform": "facebook",
    "type": "post",
    "priority": "high"
  }'
```

### Получить статистику
```bash
curl http://localhost:8000/api/stats/dashboard/ | python -m json.tool
```

### Получить все ссылки
```bash
curl http://localhost:8000/api/links/ | python -m json.tool
```

## Troubleshooting

### Порт 8000 занят?
```bash
# Изменить порт в .env
echo "BACKEND_PORT=8001" >> .env
docker-compose down
docker-compose up -d
```

### Проблемы с Docker?
```bash
# Перезапустить Docker Desktop
# Затем
docker-compose down
docker-compose up --build
```

### Backend не отвечает?
```bash
# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs backend

# Перезапустить
docker-compose restart backend
```

## Полезные команды

```bash
# Django shell
docker-compose exec backend python manage.py shell

# Bash в контейнере
docker-compose exec backend bash

# Создать миграции (если изменили модели)
docker-compose exec backend python manage.py makemigrations

# Применить миграции
docker-compose exec backend python manage.py migrate

# Запустить тесты
docker-compose exec backend python manage.py test
```

## Документация

- **README.md** - Полная документация
- **API_EXAMPLES.md** - Примеры API запросов
- **QUICK_REFERENCE.md** - Быстрая справка
- **PROJECT_SUMMARY.md** - Обзор проекта
- **CHECKLIST.md** - Что реализовано

## Статус сервисов

Проверить что всё работает:
```bash
docker-compose ps
```

Должно показать:
```
Name                     State
----------------------------------------
phil-backend_backend_1     Up
phil-backend_celery_1      Up
phil-backend_celery-beat_1 Up
phil-backend_db_1          Up
phil-backend_redis_1       Up
```

---

## 🎉 Готово!

Backend запущен и готов к работе!

**API доступен по адресу:** http://localhost:8000/api/

**Следующий шаг:** Подключите frontend и начните интеграцию!
