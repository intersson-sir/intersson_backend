# 📝 ДЛЯ МЕНЕДЖЕРА: Передайте Frontend команде

## Что готово

Backend для Phil CRM системы **полностью готов** к интеграции с Next.js frontend.

---

## 🎯 Шаг 1: Запуск Backend (уже сделано)

Backend уже запущен и доступен по адресу:
```
http://localhost:8000
```

Если backend не запущен, выполните:
```bash
cd phil-backend
./start.sh
```

---

## 📨 Шаг 2: Что отдать Frontend разработчику

### Отправьте ему этот файл:
📄 **FRONTEND_INTEGRATION.md** - полная инструкция по интеграции

### Коротко для frontend команды:

**1. Настройте environment (.env.local):**
```env
NEXT_PUBLIC_USE_MOCK=false
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**2. Base URL для всех запросов:**
```
http://localhost:8000/api
```

**3. Основные endpoints:**
```
GET    /api/links/                     → Список ссылок
POST   /api/links/                     → Создать ссылку
PATCH  /api/links/{id}/                → Обновить ссылку
DELETE /api/links/{id}/                → Удалить ссылку
POST   /api/links/bulk-update-status/  → Bulk обновление
GET    /api/stats/dashboard/           → Статистика
```

**4. Формат данных - точно как ожидает frontend:**
- Даты: ISO 8601 (`"2026-02-17T10:30:00Z"`)
- ID: UUID строки
- Content-Type: `application/json`

**5. Все фильтры работают:**
```
?platform=facebook&status=active&priority=high&search=keyword
```

---

## ✅ Checklist для Frontend

Передайте frontend команде эти пункты для проверки:

- [ ] Установить `NEXT_PUBLIC_API_URL=http://localhost:8000` в `.env.local`
- [ ] Убрать моки: `NEXT_PUBLIC_USE_MOCK=false`
- [ ] Проверить доступность API: открыть http://localhost:8000/api/links/
- [ ] Интегрировать fetch/axios с базовым URL
- [ ] Проверить CRUD операции
- [ ] Проверить фильтрацию
- [ ] Проверить bulk операции
- [ ] Проверить загрузку статистики

---

## 🧪 Быстрый тест

Frontend разработчик может проверить API прямо в браузере:

**Открыть в браузере:**
```
http://localhost:8000/api/links/
http://localhost:8000/api/stats/dashboard/
```

**Или через curl:**
```bash
curl http://localhost:8000/api/links/
```

---

## 📚 Документация для Frontend

Вся документация находится в папке `phil-backend/`:

1. **FRONTEND_INTEGRATION.md** ← Главная инструкция
2. **API_EXAMPLES.md** - примеры всех запросов
3. **README.md** - полная документация backend

---

## 🚨 Если что-то не работает

### Backend не отвечает:
```bash
cd phil-backend
docker-compose ps              # Проверить статус
docker-compose logs backend    # Посмотреть логи
docker-compose restart backend # Перезапустить
```

### CORS ошибки:
Backend уже настроен на `http://localhost:3000`, но если frontend на другом порту:
```bash
# Открыть .env в phil-backend/
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Перезапустить
docker-compose restart backend
```

---

## 📞 Что делать дальше

1. ✅ Отправьте **FRONTEND_INTEGRATION.md** frontend команде
2. ✅ Убедитесь что backend запущен (`./start.sh`)
3. ✅ Попросите frontend проверить доступность API
4. ✅ Дайте frontend команде начать интеграцию

---

## 📊 Статус

- ✅ Backend работает
- ✅ API готов
- ✅ CORS настроен
- ✅ Документация готова
- ✅ Примеры кода подготовлены

**Можно начинать интеграцию!** 🚀
