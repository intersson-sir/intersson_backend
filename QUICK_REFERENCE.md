# Quick Reference Guide

## Quick Commands

```bash
# Start everything
./start.sh

# Or manually
docker-compose up -d

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# View logs
docker-compose logs -f backend

# Stop everything
docker-compose down

# Test API
./test_api.sh
```

## Environment Variables Quick Reference

```env
# Essential
DEBUG=True
SECRET_KEY=change-this-key
DATABASE_URL=postgresql://user:pass@db:5432/phil

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Celery
ENABLE_URL_CHECK_TASK=False
```

## API Quick Reference

### Base URL
```
http://localhost:8000/api
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /links/ | List all links |
| POST | /links/ | Create link |
| GET | /links/{id}/ | Get single link |
| PATCH | /links/{id}/ | Update link |
| DELETE | /links/{id}/ | Delete link |
| POST | /links/bulk-update-status/ | Bulk status update |
| POST | /links/bulk-assign-manager/ | Bulk manager assign |
| GET | /stats/dashboard/ | Dashboard stats |
| GET | /stats/platform/{platform}/ | Platform stats |

### Filters

Add to query string:
- `?platform=facebook`
- `?status=active`
- `?priority=high`
- `?manager=John%20Doe`
- `?dateFrom=2026-01-01`
- `?dateTo=2026-02-01`
- `?search=keyword`

### Choices

**Platforms:** facebook, twitter, youtube, reddit, other

**Statuses:** active, removed, in_work, pending

**Priorities:** low, medium, high

**Types:** post, comment, video, article

## Model Fields

```python
{
  "id": "uuid",                    # Auto-generated
  "url": "string",                 # Required
  "platform": "choice",            # Required
  "type": "choice",                # Required
  "status": "choice",              # Default: pending
  "detected_at": "datetime",       # Auto
  "removed_at": "datetime|null",   # Auto on status=removed
  "priority": "choice",            # Default: medium
  "manager": "string|null",
  "notes": "text|null",
  "created_at": "datetime",        # Auto
  "updated_at": "datetime"         # Auto
}
```

## Docker Commands

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f [service]

# Execute command
docker-compose exec backend [command]

# Shell
docker-compose exec backend python manage.py shell

# Bash
docker-compose exec backend bash

# Restart
docker-compose restart backend
```

## Django Commands

```bash
# All commands must be run inside container:
docker-compose exec backend python manage.py [command]

# Common commands:
migrate                  # Apply migrations
makemigrations          # Create migrations
createsuperuser         # Create admin user
shell                   # Django shell
dbshell                 # Database shell
collectstatic           # Collect static files
test                    # Run tests
```

## Troubleshooting

### Backend won't start
```bash
docker-compose logs backend
docker-compose restart backend
```

### Database issues
```bash
docker-compose down
docker-compose up -d db
docker-compose exec backend python manage.py migrate
```

### Reset everything
```bash
docker-compose down -v  # WARNING: Deletes all data!
docker-compose up --build
```

### Port already in use
```bash
# Change in .env:
BACKEND_PORT=8001
POSTGRES_PORT=5433
```

## File Structure

```
phil-backend/
├── docker-compose.yml       # Docker config
├── Dockerfile              # Backend image
├── requirements.txt        # Python deps
├── manage.py              # Django CLI
├── start.sh               # Quick start
├── test_api.sh            # API tests
├── .env                   # Your config
├── .env.example           # Config template
├── phil/                  # Django project
│   ├── settings.py       # Settings
│   ├── urls.py           # Main routes
│   └── celery.py         # Celery config
├── links/                 # Links app
│   ├── models.py         # NegativeLink model
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   ├── filters.py        # Filters
│   ├── admin.py          # Admin interface
│   └── tasks.py          # Celery tasks
└── stats/                 # Stats app
    ├── views.py          # Stats API
    └── urls.py           # Stats routes
```

## Integration with Frontend

Frontend should set:
```env
NEXT_PUBLIC_USE_MOCK=false
NEXT_PUBLIC_API_URL=http://localhost:8000
```

API returns:
- ✅ ISO 8601 dates
- ✅ String UUIDs
- ✅ Proper HTTP codes
- ✅ JSON responses
- ✅ CORS enabled

## Production Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Update CORS_ALLOWED_ORIGINS
- [ ] Use managed PostgreSQL
- [ ] Use managed Redis
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review logs
