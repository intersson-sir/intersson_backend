# 🎯 Инструкция по интеграции Frontend с Backend

## Для Frontend разработчика

Backend Phil CRM полностью готов к интеграции. Следуйте этим шагам для подключения.

---

## ✅ Шаг 1: Настройте переменные окружения

В вашем Next.js проекте создайте/обновите файл `.env.local`:

```env
NEXT_PUBLIC_USE_MOCK=false
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔌 Шаг 2: Backend API Endpoints

Backend запущен на **http://localhost:8000** и предоставляет следующие endpoints:

### CRUD операции

```
GET    http://localhost:8000/api/links/           # Список всех ссылок
GET    http://localhost:8000/api/links/{id}/      # Одна ссылка
POST   http://localhost:8000/api/links/           # Создать ссылку
PATCH  http://localhost:8000/api/links/{id}/      # Обновить ссылку
DELETE http://localhost:8000/api/links/{id}/      # Удалить ссылку
```

### Bulk операции

```
POST   http://localhost:8000/api/links/bulk-update-status/     # Массовое обновление статуса
POST   http://localhost:8000/api/links/bulk-assign-manager/    # Массовое назначение менеджера
```

### Статистика

```
GET    http://localhost:8000/api/stats/dashboard/              # Общая статистика
GET    http://localhost:8000/api/stats/platform/{platform}/    # Статистика по платформе
```

---

## 📊 Шаг 3: Формат данных

### NegativeLink объект

**Ответ от API:**
```typescript
interface NegativeLink {
  id: string;                    // UUID в виде строки
  url: string;                   // URL контента
  platform: 'facebook' | 'twitter' | 'youtube' | 'reddit' | 'other';
  type: 'post' | 'comment' | 'video' | 'article';
  status: 'active' | 'removed' | 'in_work' | 'pending';
  detected_at: string;           // ISO 8601: "2026-02-17T10:30:00Z"
  removed_at: string | null;     // ISO 8601 или null
  priority: 'low' | 'medium' | 'high';
  manager: string | null;        // Имя менеджера или null
  notes: string | null;          // Заметки или null
  created_at: string;            // ISO 8601
  updated_at: string;            // ISO 8601
}
```

**Пример создания ссылки (POST /api/links/):**
```json
{
  "url": "https://facebook.com/negative-post",
  "platform": "facebook",
  "type": "post",
  "priority": "high",
  "manager": "John Doe",
  "notes": "Urgent removal"
}
```

**Пример обновления (PATCH /api/links/{id}/):**
```json
{
  "status": "removed",
  "notes": "Successfully removed"
}
```

### Dashboard Stats

**Ответ от GET /api/stats/dashboard/:**
```typescript
interface DashboardStats {
  total: number;
  active: number;
  removed: number;
  in_work: number;
  pending: number;
  new_last_7_days: number;
  removed_last_7_days: number;
  platforms: Array<{
    platform: string;
    total: number;
    active: number;
    removed: number;
    in_work: number;
    new_last_7_days: number;
  }>;
  activity_chart: Array<{
    date: string;              // "YYYY-MM-DD"
    active: number;
    removed: number;
  }>;
}
```

### Bulk операции

**Bulk Update Status (POST /api/links/bulk-update-status/):**
```json
{
  "ids": ["uuid1", "uuid2", "uuid3"],
  "status": "removed"
}
```

**Bulk Assign Manager (POST /api/links/bulk-assign-manager/):**
```json
{
  "ids": ["uuid1", "uuid2", "uuid3"],
  "manager": "Jane Smith"
}
```

---

## 🔍 Шаг 4: Фильтрация и поиск

### Query параметры

Все фильтры добавляются как query параметры к GET /api/links/:

```
?platform=facebook          # Фильтр по платформе
?status=active              # Фильтр по статусу
?priority=high              # Фильтр по приоритету
?manager=John%20Doe         # Фильтр по менеджеру
?dateFrom=2026-01-01        # Дата от (detected_at)
?dateTo=2026-02-17          # Дата до (detected_at)
?search=example.com         # Поиск по URL (частичное совпадение)
```

### Примеры запросов

**Все активные ссылки Facebook с высоким приоритетом:**
```
GET http://localhost:8000/api/links/?platform=facebook&status=active&priority=high
```

**Поиск ссылок за последний месяц:**
```
GET http://localhost:8000/api/links/?dateFrom=2026-01-17&dateTo=2026-02-17
```

**Комбинированный фильтр:**
```
GET http://localhost:8000/api/links/?platform=twitter&status=in_work&manager=John&search=tweet
```

---

## 🛠️ Шаг 5: Примеры кода для Frontend

### Fetch API (Vanilla JS)

```javascript
const API_URL = 'http://localhost:8000/api';

// Получить все ссылки
async function getLinks() {
  const response = await fetch(`${API_URL}/links/`);
  const data = await response.json();
  return data;
}

// Создать ссылку
async function createLink(linkData) {
  const response = await fetch(`${API_URL}/links/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(linkData),
  });
  return await response.json();
}

// Обновить ссылку
async function updateLink(id, updates) {
  const response = await fetch(`${API_URL}/links/${id}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updates),
  });
  return await response.json();
}

// Удалить ссылку
async function deleteLink(id) {
  await fetch(`${API_URL}/links/${id}/`, {
    method: 'DELETE',
  });
}

// Bulk update status
async function bulkUpdateStatus(ids, status) {
  const response = await fetch(`${API_URL}/links/bulk-update-status/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ids, status }),
  });
  return await response.json();
}

// Получить статистику
async function getDashboardStats() {
  const response = await fetch(`${API_URL}/stats/dashboard/`);
  return await response.json();
}
```

### Axios (если используете)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// CRUD
export const getLinks = (params) => api.get('/links/', { params });
export const getLink = (id) => api.get(`/links/${id}/`);
export const createLink = (data) => api.post('/links/', data);
export const updateLink = (id, data) => api.patch(`/links/${id}/`, data);
export const deleteLink = (id) => api.delete(`/links/${id}/`);

// Bulk
export const bulkUpdateStatus = (ids, status) => 
  api.post('/links/bulk-update-status/', { ids, status });
export const bulkAssignManager = (ids, manager) => 
  api.post('/links/bulk-assign-manager/', { ids, manager });

// Stats
export const getDashboardStats = () => api.get('/stats/dashboard/');
export const getPlatformStats = (platform) => api.get(`/stats/platform/${platform}/`);
```

### React Query (рекомендуется)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_URL = 'http://localhost:8000/api';

// Получить ссылки
export function useLinks(filters = {}) {
  return useQuery({
    queryKey: ['links', filters],
    queryFn: async () => {
      const params = new URLSearchParams(filters);
      const response = await fetch(`${API_URL}/links/?${params}`);
      return response.json();
    },
  });
}

// Создать ссылку
export function useCreateLink() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data) => {
      const response = await fetch(`${API_URL}/links/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['links'] });
    },
  });
}

// Обновить ссылку
export function useUpdateLink() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, data }) => {
      const response = await fetch(`${API_URL}/links/${id}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['links'] });
    },
  });
}

// Статистика
export function useDashboardStats() {
  return useQuery({
    queryKey: ['stats', 'dashboard'],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/stats/dashboard/`);
      return response.json();
    },
  });
}
```

---

## ⚙️ Шаг 6: Работа с датами

Backend возвращает даты в формате **ISO 8601**: `"2026-02-17T10:30:00Z"`

### Парсинг дат (date-fns)

```typescript
import { parseISO, format } from 'date-fns';

// Парсинг даты из API
const date = parseISO(link.detected_at);

// Форматирование для отображения
const formatted = format(date, 'dd MMM yyyy, HH:mm');
// → "17 Feb 2026, 10:30"

// Относительное время
import { formatDistanceToNow } from 'date-fns';
const relative = formatDistanceToNow(date, { addSuffix: true });
// → "2 hours ago"
```

---

## 🧪 Шаг 7: Тестирование API

### Проверка доступности

```bash
# Проверить что backend запущен
curl http://localhost:8000/api/links/

# Должен вернуть JSON с пустым массивом или списком ссылок
```

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
curl http://localhost:8000/api/stats/dashboard/ | jq
```

---

## 🚨 Обработка ошибок

### HTTP Status Codes

```typescript
200 OK          // Успешный GET/PATCH
201 Created     // Успешный POST
204 No Content  // Успешный DELETE
400 Bad Request // Ошибка валидации
404 Not Found   // Объект не найден
500 Server Error // Ошибка сервера
```

### Пример обработки ошибок

```typescript
async function createLink(data) {
  try {
    const response = await fetch(`${API_URL}/links/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create link');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating link:', error);
    throw error;
  }
}
```

---

## 📋 Шаг 8: Checklist для интеграции

- [ ] Обновил `.env.local` с правильными URL
- [ ] Backend запущен на `http://localhost:8000`
- [ ] Проверил доступность API (curl или браузер)
- [ ] Настроил API клиент (fetch/axios/react-query)
- [ ] Реализовал типы TypeScript для данных
- [ ] Добавил обработку ошибок
- [ ] Проверил парсинг дат (ISO 8601)
- [ ] Протестировал все CRUD операции
- [ ] Проверил работу фильтров
- [ ] Проверил bulk операции
- [ ] Проверил загрузку статистики

---

## 🐛 Troubleshooting

### Backend недоступен

```bash
# Проверить что Docker контейнеры запущены
cd phil-backend
docker-compose ps

# Если нет, запустить
./start.sh
```

### CORS ошибки

Убедитесь что в `.env` backend установлено:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Ошибки 404

Проверьте правильность URL:
- ✅ `http://localhost:8000/api/links/`
- ❌ `http://localhost:8000/links/` (нет /api/)

### Ошибки валидации (400)

Проверьте что отправляете правильные данные:
- `platform` должен быть одним из: facebook, twitter, youtube, reddit, other
- `type` должен быть одним из: post, comment, video, article
- `status` должен быть одним из: active, removed, in_work, pending
- `priority` должен быть одним из: low, medium, high

---

## 📞 Контакты

При возникновении проблем:
1. Проверьте backend логи: `docker-compose logs -f backend`
2. Проверьте документацию: `phil-backend/README.md`
3. Используйте тестовый скрипт: `./test_api.sh`

---

## ✨ Готово!

Backend полностью готов к работе. После выполнения всех шагов ваш Frontend должен успешно интегрироваться с API.

**Base URL:** http://localhost:8000/api

**Документация API:** Откройте http://localhost:8000/api/ в браузере для интерактивной документации.
