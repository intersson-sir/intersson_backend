#!/bin/bash

echo "🚀 Phil Backend - Quick Start Script"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please review and update .env file with your settings!"
    echo "   Especially change SECRET_KEY for production use."
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build and start services
echo "🏗️  Building Docker containers..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Wait for database
echo "   Waiting for PostgreSQL..."
until docker-compose exec -T db pg_isready -U phil_user -d phil > /dev/null 2>&1; do
    sleep 1
done
echo "   ✅ PostgreSQL is ready"

# Wait for backend
echo "   Waiting for backend..."
sleep 3
echo "   ✅ Backend is ready"

echo ""
echo "📊 Running database migrations..."
docker-compose exec -T backend python manage.py migrate

echo ""
echo "📦 Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

echo ""
echo "✅ Phil Backend is ready!"
echo ""
echo "📍 API Endpoints:"
echo "   - API Root:     http://localhost:8000/api/"
echo "   - Links:        http://localhost:8000/api/links/"
echo "   - Statistics:   http://localhost:8000/api/stats/dashboard/"
echo "   - Admin Panel:  http://localhost:8000/admin/"
echo ""
echo "📖 Next steps:"
echo "   1. Create a superuser:  docker-compose exec backend python manage.py createsuperuser"
echo "   2. View logs:           docker-compose logs -f"
echo "   3. Stop services:       docker-compose down"
echo ""
echo "📚 Documentation:"
echo "   - README.md for full documentation"
echo "   - API_EXAMPLES.md for API usage examples"
echo ""
echo "🎉 Happy coding!"
