#!/bin/bash

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis to be ready..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist (optional, for development)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL || true
fi

# Start server
echo "Starting Gunicorn..."
exec gunicorn phil.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
