# Phil Backend API Examples

## Базовые операции

### Получить все ссылки
```bash
curl http://localhost:8000/api/links/
```

### Получить ссылку по ID
```bash
curl http://localhost:8000/api/links/{uuid}/
```

### Создать новую ссылку
```bash
curl -X POST http://localhost:8000/api/links/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://facebook.com/negative-post-123",
    "platform": "facebook",
    "type": "post",
    "status": "active",
    "priority": "high",
    "manager": "John Doe",
    "notes": "Urgent removal required"
  }'
```

### Обновить ссылку (частично)
```bash
curl -X PATCH http://localhost:8000/api/links/{uuid}/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "removed",
    "notes": "Successfully removed by Facebook support"
  }'
```

### Удалить ссылку
```bash
curl -X DELETE http://localhost:8000/api/links/{uuid}/
```

## Фильтрация

### По платформе
```bash
curl "http://localhost:8000/api/links/?platform=facebook"
```

### По статусу
```bash
curl "http://localhost:8000/api/links/?status=active"
```

### По приоритету
```bash
curl "http://localhost:8000/api/links/?priority=high"
```

### По менеджеру
```bash
curl "http://localhost:8000/api/links/?manager=John%20Doe"
```

### По диапазону дат
```bash
curl "http://localhost:8000/api/links/?dateFrom=2026-01-01&dateTo=2026-02-01"
```

### Поиск по URL
```bash
curl "http://localhost:8000/api/links/?search=facebook.com"
```

### Комбинированные фильтры
```bash
curl "http://localhost:8000/api/links/?platform=facebook&status=active&priority=high&manager=John%20Doe"
```

## Bulk операции

### Массовое обновление статуса
```bash
curl -X POST http://localhost:8000/api/links/bulk-update-status/ \
  -H "Content-Type: application/json" \
  -d '{
    "ids": [
      "550e8400-e29b-41d4-a716-446655440000",
      "550e8400-e29b-41d4-a716-446655440001"
    ],
    "status": "removed"
  }'
```

### Массовое назначение менеджера
```bash
curl -X POST http://localhost:8000/api/links/bulk-assign-manager/ \
  -H "Content-Type: application/json" \
  -d '{
    "ids": [
      "550e8400-e29b-41d4-a716-446655440000",
      "550e8400-e29b-41d4-a716-446655440001"
    ],
    "manager": "Jane Smith"
  }'
```

## Статистика

### Общая статистика
```bash
curl http://localhost:8000/api/stats/dashboard/
```

**Ответ:**
```json
{
  "total": 100,
  "active": 25,
  "removed": 50,
  "in_work": 15,
  "pending": 10,
  "new_last_7_days": 12,
  "removed_last_7_days": 8,
  "platforms": [
    {
      "platform": "facebook",
      "total": 30,
      "active": 10,
      "removed": 15,
      "in_work": 3,
      "new_last_7_days": 5
    }
  ],
  "activity_chart": [
    {
      "date": "2026-02-01",
      "active": 3,
      "removed": 5
    }
  ]
}
```

### Статистика по платформе
```bash
curl http://localhost:8000/api/stats/platform/facebook/
```

**Ответ:**
```json
{
  "platform": "facebook",
  "total": 30,
  "active": 10,
  "removed": 15,
  "in_work": 3,
  "new_last_7_days": 5
}
```

## Примеры с jq (форматирование JSON)

Если у вас установлен jq:

```bash
# Красивый вывод JSON
curl http://localhost:8000/api/links/ | jq

# Получить только URL всех активных ссылок
curl "http://localhost:8000/api/links/?status=active" | jq '.results[].url'

# Количество активных ссылок
curl "http://localhost:8000/api/links/?status=active" | jq '.count'
```

## Примеры с Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Получить все ссылки
response = requests.get(f"{BASE_URL}/links/")
links = response.json()

# Создать ссылку
new_link = {
    "url": "https://twitter.com/negative-tweet",
    "platform": "twitter",
    "type": "post",
    "priority": "high"
}
response = requests.post(f"{BASE_URL}/links/", json=new_link)
created_link = response.json()

# Обновить статус
link_id = created_link['id']
response = requests.patch(
    f"{BASE_URL}/links/{link_id}/",
    json={"status": "in_work", "manager": "John Doe"}
)

# Bulk обновление
response = requests.post(
    f"{BASE_URL}/links/bulk-update-status/",
    json={"ids": [link_id], "status": "removed"}
)

# Получить статистику
response = requests.get(f"{BASE_URL}/stats/dashboard/")
stats = response.json()
print(f"Total links: {stats['total']}")
```

## Примеры с JavaScript fetch

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Получить все ссылки
fetch(`${BASE_URL}/links/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Создать ссылку
fetch(`${BASE_URL}/links/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://youtube.com/negative-video',
    platform: 'youtube',
    type: 'video',
    priority: 'medium'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Фильтрация
const params = new URLSearchParams({
  platform: 'facebook',
  status: 'active',
  priority: 'high'
});

fetch(`${BASE_URL}/links/?${params}`)
  .then(response => response.json())
  .then(data => console.log(data));
```
