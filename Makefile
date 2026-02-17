.PHONY: help build up down logs shell migrate makemigrations createsuperuser test clean

help:
	@echo "Phil Backend - Makefile Commands"
	@echo ""
	@echo "  make build          - Build Docker containers"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - Show logs (all services)"
	@echo "  make logs-backend   - Show backend logs"
	@echo "  make logs-celery    - Show celery logs"
	@echo "  make shell          - Open Django shell"
	@echo "  make bash           - Open bash in backend container"
	@echo "  make migrate        - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Stop and remove all containers and volumes"
	@echo "  make restart        - Restart all services"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started! Backend available at http://localhost:8000"

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-celery:
	docker-compose logs -f celery

logs-db:
	docker-compose logs -f db

shell:
	docker-compose exec backend python manage.py shell

bash:
	docker-compose exec backend bash

migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

test:
	docker-compose exec backend python manage.py test

test-coverage:
	docker-compose exec backend coverage run --source='.' manage.py test
	docker-compose exec backend coverage report

clean:
	docker-compose down -v
	@echo "All containers and volumes removed!"

restart:
	docker-compose restart

restart-backend:
	docker-compose restart backend

ps:
	docker-compose ps

collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput
