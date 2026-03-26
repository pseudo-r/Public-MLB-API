"""Data ingestion services for MLB Stats API data.

Each service class fetches data from the API client and performs
idempotent upserts into the database using update_or_create.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import structlog
from django.db import transaction

from apps.core.exceptions import IngestionError
from apps.mlb.models import Game, Player, Standing, Team, Transaction, Venue
from clients.mlb_client import MLBClient, get_mlb_client

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class IngestionResult:
    """Result of an ingestion operation."""

    created: int = 0
    updated: int = 0
    errors: int = 0
    details: list[str] = field(default_factory=list)

    @property
    def total_processed(self) -> int:
        return self.created + self.updated

    def to_dict(self) -> dict[str, Any]:
        return {
            "created": self.created,
            "updated": self.updated,
            "errors": self.errors,
            "total_processed": self.total_processed,
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# Team ingestion
# ---------------------------------------------------------------------------


class TeamIngestionService:
    """Ingest MLB teams from /teams."""

    def __init__(self, client: MLBClient | None = None) -> None:
        self.client = client or get_mlb_client()

    def _parse_team(self, t: dict[str, Any]) -> dict[str, Any]:
        venue_data = t.get("venue") or {}
        league_data = t.get("league") or {}
        division_data = t.get("division") or {}
        return {
            "name": t.get("name", ""),
            "team_name": t.get("teamName", ""),
            "location_name": t.get("locationName", ""),
            "abbreviation": t.get("abbreviation", ""),
            "team_code": t.get("teamCode", ""),
            "file_code": t.get("fileCode", ""),
            "league_id": league_data.get("id"),
            "league_name": league_data.get("name", ""),
            "division_id": division_data.get("id"),
            "division_name": division_data.get("name", ""),
            "sport_id": (t.get("sport") or {}).get("id", 1),
            "first_year_of_play": t.get("firstYearOfPlay", ""),
            "active": t.get("active", True),
            "raw_data": t,
            "_venue_id": venue_data.get("id"),
        }

    @transaction.atomic
    def ingest_teams(self, sport_id: int = 1) -> IngestionResult:
        """Fetch and upsert all MLB teams."""
        result = IngestionResult()
        try:
            response = self.client.get_teams(sport_id=sport_id)
            teams_data: list[dict[str, Any]] = response.data.get("teams", [])

            if not teams_data:
                logger.warning("no_teams_found", sport_id=sport_id)
                return result

            for t in teams_data:
                try:
                    mlb_id = t.get("id")
                    if not mlb_id:
                        result.errors += 1
                        continue

                    parsed = self._parse_team(t)
                    venue_id = parsed.pop("_venue_id", None)

                    # Resolve venue FK if we have it stored
                    venue_obj = Venue.objects.filter(mlb_id=venue_id).first() if venue_id else None

                    _, created = Team.objects.update_or_create(
                        mlb_id=mlb_id,
                        defaults={**parsed, "venue": venue_obj},
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1

                except Exception as e:
                    logger.error("team_parse_error", mlb_id=t.get("id"), error=str(e))
                    result.errors += 1

            logger.info(
                "teams_ingested",
                created=result.created,
                updated=result.updated,
                errors=result.errors,
            )

        except Exception as e:
            logger.exception("team_ingestion_failed")
            raise IngestionError(f"Failed to ingest teams: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Venue ingestion
# ---------------------------------------------------------------------------


class VenueIngestionService:
    """Ingest MLB venues from /venues."""

    def __init__(self, client: MLBClient | None = None) -> None:
        self.client = client or get_mlb_client()

    @transaction.atomic
    def ingest_venues(self, sport_id: int = 1) -> IngestionResult:
        """Fetch and upsert all MLB venues."""
        result = IngestionResult()
        try:
            response = self.client.get_venues(sport_id=sport_id, hydrate="location,fieldInfo")
            venues_data: list[dict[str, Any]] = response.data.get("venues", [])

            for v in venues_data:
                try:
                    mlb_id = v.get("id")
                    if not mlb_id:
                        result.errors += 1
                        continue

                    location = v.get("location") or {}
                    field_info = v.get("fieldInfo") or {}

                    _, created = Venue.objects.update_or_create(
                        mlb_id=mlb_id,
                        defaults={
                            "name": v.get("name", ""),
                            "city": location.get("city", ""),
                            "state": location.get("stateAbbrev", "") or location.get("state", ""),
                            "country": location.get("country", "USA"),
                            "capacity": field_info.get("capacity"),
                            "roof_type": field_info.get("roofType", {}).get("description", ""),
                            "turf_type": field_info.get("turfType", {}).get("description", ""),
                            "left_line": field_info.get("leftLine"),
                            "left_center": field_info.get("leftCenter"),
                            "center": field_info.get("center"),
                            "right_center": field_info.get("rightCenter"),
                            "right_line": field_info.get("rightLine"),
                            "latitude": location.get("defaultCoordinates", {}).get("latitude"),
                            "longitude": location.get("defaultCoordinates", {}).get("longitude"),
                            "active": v.get("active", True),
                            "raw_data": v,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1

                except Exception as e:
                    logger.error("venue_parse_error", mlb_id=v.get("id"), error=str(e))
                    result.errors += 1

            logger.info("venues_ingested", created=result.created, updated=result.updated)

        except Exception as e:
            logger.exception("venue_ingestion_failed")
            raise IngestionError(f"Failed to ingest venues: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Schedule ingestion
# ---------------------------------------------------------------------------


class ScheduleIngestionService:
    """Ingest games from /schedule for a given date."""

    def __init__(self, client: MLBClient | None = None) -> None:
        self.client = client or get_mlb_client()

    _STATUS_MAP = {
        "final": Game.STATUS_FINAL,
        "game over": Game.STATUS_FINAL,
        "completed": Game.STATUS_FINAL,
        "in progress": Game.STATUS_IN_PROGRESS,
        "scheduled": Game.STATUS_SCHEDULED,
        "pre-game": Game.STATUS_SCHEDULED,
        "postponed": Game.STATUS_POSTPONED,
        "suspended": Game.STATUS_SUSPENDED,
        "cancelled": Game.STATUS_CANCELLED,
    }

    def _normalize_status(self, detailed_state: str) -> str:
        return self._STATUS_MAP.get(detailed_state.lower(), Game.STATUS_SCHEDULED)

    @transaction.atomic
    def ingest_schedule(
        self,
        date_str: str | None = None,
        sport_id: int = 1,
        season: int | None = None,
    ) -> IngestionResult:
        """Fetch and upsert games for a date (defaults to today)."""
        result = IngestionResult()
        if not date_str:
            date_str = date.today().isoformat()

        try:
            response = self.client.get_schedule(
                sport_id=sport_id,
                date=date_str,
                hydrate="venue,linescore",
            )
            dates_data: list[dict[str, Any]] = response.data.get("dates", [])

            for date_block in dates_data:
                for game_data in date_block.get("games", []):
                    try:
                        game_pk = game_data.get("gamePk")
                        if not game_pk:
                            result.errors += 1
                            continue

                        status_obj = game_data.get("status") or {}
                        detailed_state = status_obj.get("detailedState", "")
                        status = self._normalize_status(detailed_state)

                        home_data = (game_data.get("teams") or {}).get("home", {}).get("team", {})
                        away_data = (game_data.get("teams") or {}).get("away", {}).get("team", {})

                        home_team = Team.objects.filter(mlb_id=home_data.get("id")).first()
                        away_team = Team.objects.filter(mlb_id=away_data.get("id")).first()

                        if not home_team or not away_team:
                            logger.warning("teams_not_found", game_pk=game_pk)
                            result.errors += 1
                            continue

                        venue_data = game_data.get("venue") or {}
                        venue_obj = (
                            Venue.objects.filter(mlb_id=venue_data.get("id")).first()
                            if venue_data.get("id")
                            else None
                        )

                        # Parse game date
                        date_raw = game_data.get("gameDate", "")
                        try:
                            game_date = datetime.fromisoformat(date_raw.replace("Z", "+00:00"))
                        except (ValueError, TypeError):
                            game_date = datetime.now()

                        # Scores from linescore
                        linescore = game_data.get("linescore") or {}
                        teams_ls = linescore.get("teams") or {}
                        home_score = (teams_ls.get("home") or {}).get("runs")
                        away_score = (teams_ls.get("away") or {}).get("runs")

                        season_val = game_data.get("season") or (season or game_date.year)
                        official_date_str = game_data.get("officialDate") or date_str

                        _, created = Game.objects.update_or_create(
                            mlb_pk=game_pk,
                            defaults={
                                "game_date": game_date,
                                "official_date": official_date_str,
                                "game_type": game_data.get("gameType", "R"),
                                "season": season_val,
                                "series_description": game_data.get("seriesDescription", ""),
                                "home_team": home_team,
                                "away_team": away_team,
                                "venue": venue_obj,
                                "status": status,
                                "detailed_state": detailed_state,
                                "home_score": home_score,
                                "away_score": away_score,
                                "current_inning": linescore.get("currentInning"),
                                "inning_state": linescore.get("inningState", ""),
                                "double_header": game_data.get("doubleHeader", "N"),
                                "game_number": game_data.get("gameNumber", 1),
                                "raw_data": game_data,
                            },
                        )
                        if created:
                            result.created += 1
                        else:
                            result.updated += 1

                    except Exception as e:
                        logger.error("game_parse_error", game_pk=game_data.get("gamePk"), error=str(e))
                        result.errors += 1

            logger.info(
                "schedule_ingested",
                date=date_str,
                created=result.created,
                updated=result.updated,
                errors=result.errors,
            )

        except Exception as e:
            logger.exception("schedule_ingestion_failed", date=date_str)
            raise IngestionError(f"Failed to ingest schedule: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Standings ingestion
# ---------------------------------------------------------------------------


class StandingsIngestionService:
    """Ingest standings from /standings."""

    def __init__(self, client: MLBClient | None = None) -> None:
        self.client = client or get_mlb_client()

    @transaction.atomic
    def ingest_standings(
        self,
        season: int | None = None,
        standings_type: str = "regularSeason",
    ) -> IngestionResult:
        """Fetch and upsert division standings."""
        result = IngestionResult()
        if not season:
            season = datetime.now().year

        try:
            response = self.client.get_standings(season=season, standings_type=standings_type)
            records: list[dict[str, Any]] = response.data.get("records", [])

            for record in records:
                league_id = (record.get("league") or {}).get("id")
                division_id = (record.get("division") or {}).get("id")

                for team_record in record.get("teamRecords", []):
                    try:
                        team_id = (team_record.get("team") or {}).get("id")
                        team_obj = Team.objects.filter(mlb_id=team_id).first()
                        if not team_obj:
                            result.errors += 1
                            continue

                        _, created = Standing.objects.update_or_create(
                            team=team_obj,
                            season=season,
                            standings_type=standings_type,
                            defaults={
                                "league_id": league_id,
                                "division_id": division_id,
                                "division_rank": team_record.get("divisionRank"),
                                "league_rank": team_record.get("leagueRank"),
                                "wild_card_rank": team_record.get("wildCardRank"),
                                "sport_rank": team_record.get("sportRank"),
                                "wins": team_record.get("wins", 0),
                                "losses": team_record.get("losses", 0),
                                "pct": team_record.get("winningPercentage", ""),
                                "games_back": team_record.get("gamesBack", ""),
                                "wild_card_games_back": team_record.get("wildCardGamesBack", ""),
                                "streak_code": (team_record.get("streak") or {}).get("streakCode", ""),
                                "last_ten": (team_record.get("records") or {})
                                    .get("splitRecords", [{}])[0]
                                    .get("pct", "") if team_record.get("records") else "",
                                "clinched": team_record.get("clinched", False),
                                "raw_data": team_record,
                            },
                        )
                        if created:
                            result.created += 1
                        else:
                            result.updated += 1

                    except Exception as e:
                        logger.error("standing_parse_error", error=str(e))
                        result.errors += 1

            logger.info(
                "standings_ingested",
                season=season,
                created=result.created,
                updated=result.updated,
            )

        except Exception as e:
            logger.exception("standings_ingestion_failed", season=season)
            raise IngestionError(f"Failed to ingest standings: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Transaction ingestion
# ---------------------------------------------------------------------------


class TransactionIngestionService:
    """Ingest player transactions from /transactions."""

    def __init__(self, client: MLBClient | None = None) -> None:
        self.client = client or get_mlb_client()

    @transaction.atomic
    def ingest_transactions(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        sport_id: int = 1,
    ) -> IngestionResult:
        """Fetch and upsert transactions for a date range."""
        result = IngestionResult()
        today = date.today().isoformat()
        start_date = start_date or today
        end_date = end_date or today

        try:
            response = self.client.get_transactions(
                start_date=start_date, end_date=end_date, sport_id=sport_id
            )
            txns: list[dict[str, Any]] = response.data.get("transactions", [])

            for t in txns:
                try:
                    person = t.get("person") or {}
                    to_team_data = t.get("toTeam") or {}
                    from_team_data = t.get("fromTeam") or {}

                    to_team = Team.objects.filter(mlb_id=to_team_data.get("id")).first() if to_team_data.get("id") else None
                    from_team = Team.objects.filter(mlb_id=from_team_data.get("id")).first() if from_team_data.get("id") else None

                    date_raw = t.get("date") or ""
                    eff_date_raw = t.get("effectiveDate") or ""
                    res_date_raw = t.get("resolutionDate") or ""

                    def _parse_date(s: str) -> date | None:
                        try:
                            return date.fromisoformat(s[:10]) if s else None
                        except ValueError:
                            return None

                    mlb_id = str(t.get("id") or "")
                    defaults = {
                        "person_name": person.get("fullName", ""),
                        "person_mlb_id": person.get("id"),
                        "to_team": to_team,
                        "from_team": from_team,
                        "date": _parse_date(date_raw),
                        "effective_date": _parse_date(eff_date_raw),
                        "resolution_date": _parse_date(res_date_raw),
                        "type_code": t.get("typeCode", ""),
                        "type_desc": t.get("typeDesc", ""),
                        "description": t.get("description", ""),
                        "raw_data": t,
                    }

                    if mlb_id:
                        _, created = Transaction.objects.update_or_create(
                            mlb_id=mlb_id, defaults=defaults
                        )
                    else:
                        Transaction.objects.create(mlb_id="", **defaults)
                        created = True

                    if created:
                        result.created += 1
                    else:
                        result.updated += 1

                except Exception as e:
                    logger.error("transaction_parse_error", error=str(e))
                    result.errors += 1

            logger.info(
                "transactions_ingested",
                start=start_date,
                end=end_date,
                created=result.created,
                updated=result.updated,
            )

        except Exception as e:
            logger.exception("transaction_ingestion_failed")
            raise IngestionError(f"Failed to ingest transactions: {e}") from e

        return result
