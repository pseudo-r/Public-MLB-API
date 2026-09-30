# MLB Django service

Django 5.2 LTS service for MLB Stats API data. See the [endpoint reference](../README.md) and [maintenance audit](../docs/audit-2026-09-30.md).

## Development

Use Python 3.12 or later in a virtual environment:

```sh
python -m pip install -e ".[dev]"
python manage.py migrate --settings=config.settings.local
python manage.py runserver --settings=config.settings.local
```

The test settings use an isolated SQLite database by default. CI supplies `TEST_DATABASE_URL` to exercise PostgreSQL. Run `python -m pytest` for tests and coverage, and `python -m ruff check .` for lint.

## Additional live routes

These GET routes return upstream JSON without persisting it:

- `/api/v1/live/teams/{team_id}/roster/`
- `/api/v1/live/games/{game_pk}/plays/`
- `/api/v1/live/divisions/`

The client's `get_game_feed()` uses MLB's v1.1 route; the other methods use v1. Ingestion POST endpoints require an authenticated staff user in deployment. Configure secrets, database and cache URLs before starting the production image; apply migrations to the configured database separately.
