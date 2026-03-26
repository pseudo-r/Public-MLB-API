"""Celery tasks for MLB data ingestion.

All tasks are idempotent — safe to retry or run concurrently.
"""

from __future__ import annotations

import structlog

from celery import shared_task

logger = structlog.get_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_teams_task(self, sport_id: int = 1) -> dict:
    """Ingest MLB teams (and resolve venue FKs)."""
    from apps.ingest.services import TeamIngestionService, VenueIngestionService

    try:
        # Venues first so team FK resolution works
        venue_result = VenueIngestionService().ingest_venues(sport_id=sport_id)
        team_result = TeamIngestionService().ingest_teams(sport_id=sport_id)
        logger.info(
            "teams_task_completed",
            venues_created=venue_result.created,
            teams_created=team_result.created,
            teams_updated=team_result.updated,
        )
        return {
            "venues": venue_result.to_dict(),
            "teams": team_result.to_dict(),
        }
    except Exception as exc:
        logger.error("teams_task_failed", error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_schedule_task(self, date: str | None = None, sport_id: int = 1) -> dict:
    """Ingest schedule/games for a date."""
    from apps.ingest.services import ScheduleIngestionService

    try:
        result = ScheduleIngestionService().ingest_schedule(date_str=date, sport_id=sport_id)
        logger.info(
            "schedule_task_completed",
            date=date,
            created=result.created,
            updated=result.updated,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("schedule_task_failed", date=date, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_standings_task(self, season: int | None = None) -> dict:
    """Ingest division standings for a season."""
    from apps.ingest.services import StandingsIngestionService

    try:
        result = StandingsIngestionService().ingest_standings(season=season)
        logger.info(
            "standings_task_completed",
            season=season,
            created=result.created,
            updated=result.updated,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("standings_task_failed", season=season, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_transactions_task(
    self,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """Ingest MLB player transactions for a date range."""
    from apps.ingest.services import TransactionIngestionService

    try:
        result = TransactionIngestionService().ingest_transactions(
            start_date=start_date,
            end_date=end_date,
        )
        logger.info(
            "transactions_task_completed",
            start=start_date,
            end=end_date,
            created=result.created,
            updated=result.updated,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("transactions_task_failed", start=start_date, end=end_date, error=str(exc))
        raise self.retry(exc=exc) from exc
