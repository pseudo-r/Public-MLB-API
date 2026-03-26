.PHONY: install migrate runserver test lint celery beat shell

install:
	pip install -e ".[dev]"

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

createsuperuser:
	python manage.py createsuperuser

runserver:
	python manage.py runserver 0.0.0.0:8001

test:
	python -m pytest tests/ -q

test-cov:
	python -m pytest tests/ --cov=apps --cov=clients --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .
	ruff check --fix .

celery:
	celery -A config worker -l INFO

beat:
	celery -A config beat -l INFO

shell:
	python manage.py shell

# Docker shortcuts
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f web

# Ingest shortcuts (local — calls services directly)
ingest-teams:
	python manage.py shell -c "from apps.ingest.services import TeamIngestionService, VenueIngestionService; VenueIngestionService().ingest_venues(); r = TeamIngestionService().ingest_teams(); print(r.to_dict())"

ingest-schedule:
	python manage.py shell -c "from apps.ingest.services import ScheduleIngestionService; r = ScheduleIngestionService().ingest_schedule(); print(r.to_dict())"

ingest-standings:
	python manage.py shell -c "from apps.ingest.services import StandingsIngestionService; r = StandingsIngestionService().ingest_standings(); print(r.to_dict())"
