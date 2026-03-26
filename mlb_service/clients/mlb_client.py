"""HTTP client for the MLB Stats API.

Wraps https://statsapi.mlb.com/api/v1/ with retry logic, structured
logging, and a consistent APIResponse dataclass — mirroring the
ESPNClient architecture from espn_service.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import httpx
import structlog
from django.conf import settings
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Response dataclass
# ---------------------------------------------------------------------------


@dataclass
class APIResponse:
    """Wrapper around a raw MLB Stats API response."""

    data: dict[str, Any]
    status_code: int
    url: str
    elapsed_ms: float = 0.0

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300


# ---------------------------------------------------------------------------
# MLBClient
# ---------------------------------------------------------------------------


class MLBClient:
    """Thin, retry-aware HTTP client for statsapi.mlb.com."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        user_agent: str | None = None,
    ) -> None:
        cfg = getattr(settings, "MLB_CLIENT", {})
        self.base_url = (base_url or cfg.get("BASE_URL", "https://statsapi.mlb.com/api/v1/")).rstrip(
            "/"
        )
        self.timeout = timeout or cfg.get("TIMEOUT", 30.0)
        self.max_retries = max_retries or cfg.get("MAX_RETRIES", 3)
        self.user_agent = user_agent or cfg.get(
            "USER_AGENT",
            "MLB-Service/1.0 (https://github.com/pseudo-r/Public-MLB-API)",
        )
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> MLBClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Internal request helper
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict[str, Any] | None = None) -> APIResponse:
        """Execute a GET request with retry and structured logging."""

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            reraise=True,
        )
        def _request() -> APIResponse:
            url = f"{self.base_url}/{path.lstrip('/')}"
            logger.debug("mlb_api_request", url=url, params=params)
            start = datetime.now()
            response = self._client.get(path.lstrip("/"), params=params)
            elapsed = (datetime.now() - start).total_seconds() * 1000

            logger.debug(
                "mlb_api_response",
                url=url,
                status_code=response.status_code,
                elapsed_ms=round(elapsed, 2),
            )

            if response.status_code == 429:
                logger.warning("mlb_rate_limited", url=url)
                raise httpx.HTTPStatusError(
                    "Rate limited", request=response.request, response=response
                )

            response.raise_for_status()
            return APIResponse(
                data=response.json(),
                status_code=response.status_code,
                url=str(response.url),
                elapsed_ms=round(elapsed, 2),
            )

        return _request()

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    def get_sports(self, sport_id: int | None = None) -> APIResponse:
        """GET /sports or /sports/{sportId}."""
        path = f"sports/{sport_id}" if sport_id else "sports"
        return self._get(path)

    def get_leagues(self, sport_id: int | None = None) -> APIResponse:
        """GET /leagues — optionally filter by sportId."""
        params: dict[str, Any] = {}
        if sport_id:
            params["sportId"] = sport_id
        return self._get("leagues", params)

    def get_teams(
        self,
        sport_id: int = 1,
        season: int | None = None,
        league_ids: str | None = None,
    ) -> APIResponse:
        """GET /teams — MLB teams by default (sportId=1)."""
        params: dict[str, Any] = {"sportId": sport_id}
        if season:
            params["season"] = season
        if league_ids:
            params["leagueIds"] = league_ids
        return self._get("teams", params)

    def get_team(self, team_id: int, season: int | None = None) -> APIResponse:
        """GET /teams/{teamId}."""
        params: dict[str, Any] = {}
        if season:
            params["season"] = season
        return self._get(f"teams/{team_id}", params)

    def get_schedule(
        self,
        sport_id: int = 1,
        date: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        team_id: int | None = None,
        season: int | None = None,
        game_pk: int | None = None,
        hydrate: str | None = None,
    ) -> APIResponse:
        """GET /schedule."""
        params: dict[str, Any] = {"sportId": sport_id}
        if date:
            params["date"] = date
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if team_id:
            params["teamId"] = team_id
        if season:
            params["season"] = season
        if game_pk:
            params["gamePk"] = game_pk
        if hydrate:
            params["hydrate"] = hydrate
        return self._get("schedule", params)

    def get_standings(
        self,
        league_id: str = "103,104",
        season: int | None = None,
        standings_type: str = "regularSeason",
        date: str | None = None,
    ) -> APIResponse:
        """GET /standings."""
        params: dict[str, Any] = {
            "leagueId": league_id,
            "standingsTypes": standings_type,
        }
        if season:
            params["season"] = season
        if date:
            params["date"] = date
        params.setdefault("hydrate", "team,league,division")
        return self._get("standings", params)

    def get_person(self, person_id: int, hydrate: str | None = None) -> APIResponse:
        """GET /people/{personId}."""
        params: dict[str, Any] = {}
        if hydrate:
            params["hydrate"] = hydrate
        return self._get(f"people/{person_id}", params)

    def get_person_stats(
        self,
        person_id: int,
        stats: str = "season",
        group: str = "hitting",
        season: int | None = None,
    ) -> APIResponse:
        """GET /people/{personId}/stats."""
        params: dict[str, Any] = {"stats": stats, "group": group}
        if season:
            params["season"] = season
        return self._get(f"people/{person_id}/stats", params)

    def get_transactions(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        team_id: int | None = None,
        sport_id: int = 1,
    ) -> APIResponse:
        """GET /transactions."""
        today = date.today().isoformat()
        params: dict[str, Any] = {
            "startDate": start_date or today,
            "endDate": end_date or today,
            "sportId": sport_id,
        }
        if team_id:
            params["teamId"] = team_id
        return self._get("transactions", params)

    def get_game_feed(self, game_pk: int) -> APIResponse:
        """GET /game/{gamePk}/feed/live."""
        return self._get(f"game/{game_pk}/feed/live")

    def get_game_boxscore(self, game_pk: int) -> APIResponse:
        """GET /game/{gamePk}/boxscore."""
        return self._get(f"game/{game_pk}/boxscore")

    def get_game_linescore(self, game_pk: int) -> APIResponse:
        """GET /game/{gamePk}/linescore."""
        return self._get(f"game/{game_pk}/linescore")

    def get_venues(self, sport_id: int = 1, hydrate: str | None = None) -> APIResponse:
        """GET /venues."""
        params: dict[str, Any] = {"sportId": sport_id}
        if hydrate:
            params["hydrate"] = hydrate
        return self._get("venues", params)

    def get_venue(self, venue_id: int, hydrate: str | None = None) -> APIResponse:
        """GET /venues/{venueId}."""
        params: dict[str, Any] = {}
        if hydrate:
            params["hydrate"] = hydrate
        return self._get(f"venues/{venue_id}", params)

    def get_stat_leaders(
        self,
        leader_categories: str,
        season: int | None = None,
        sport_id: int = 1,
        limit: int = 10,
    ) -> APIResponse:
        """GET /stats/leaders."""
        params: dict[str, Any] = {
            "leaderCategories": leader_categories,
            "sportId": sport_id,
            "limit": limit,
        }
        if season:
            params["season"] = season
        return self._get("stats/leaders", params)

    def get_draft(self, year: int) -> APIResponse:
        """GET /draft/{year}."""
        return self._get(f"draft/{year}")


# ---------------------------------------------------------------------------
# Singleton factory
# ---------------------------------------------------------------------------

_client_instance: MLBClient | None = None


def get_mlb_client() -> MLBClient:
    """Return a shared MLBClient instance (thread-safe for read-only use)."""
    global _client_instance
    if _client_instance is None:
        _client_instance = MLBClient()
    return _client_instance
