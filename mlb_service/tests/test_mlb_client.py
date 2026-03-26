"""Unit tests for MLBClient."""

import pytest
import httpx
from pytest_httpx import HTTPXMock

from clients.mlb_client import MLBClient


BASE = "https://statsapi.mlb.com/api/v1"


@pytest.fixture
def client():
    """MLBClient with test base URL."""
    return MLBClient(
        base_url=f"{BASE}/",
        timeout=5.0,
        max_retries=1,
    )


class TestMLBClientTeams:
    def test_get_teams_success(self, httpx_mock: HTTPXMock, client: MLBClient):
        httpx_mock.add_response(
            url=f"{BASE}/teams?sportId=1",
            json={"copyright": "...", "teams": [{"id": 119, "name": "Los Angeles Dodgers"}]},
        )
        result = client.get_teams()
        assert result.ok
        assert len(result.data["teams"]) == 1
        assert result.data["teams"][0]["id"] == 119

    def test_get_team_success(self, httpx_mock: HTTPXMock, client: MLBClient):
        httpx_mock.add_response(
            url=f"{BASE}/teams/119",
            json={"copyright": "...", "teams": [{"id": 119, "name": "Los Angeles Dodgers"}]},
        )
        result = client.get_team(119)
        assert result.ok
        assert result.data["teams"][0]["name"] == "Los Angeles Dodgers"


class TestMLBClientSchedule:
    def test_get_schedule(self, httpx_mock: HTTPXMock, client: MLBClient):
        httpx_mock.add_response(
            url=f"{BASE}/schedule?sportId=1&date=2025-04-01",
            json={
                "copyright": "...",
                "dates": [{"date": "2025-04-01", "games": [{"gamePk": 745444}]}],
            },
        )
        result = client.get_schedule(date="2025-04-01")
        assert result.ok
        assert result.data["dates"][0]["games"][0]["gamePk"] == 745444


class TestMLBClientStandings:
    def test_get_standings(self, httpx_mock: HTTPXMock, client: MLBClient):
        httpx_mock.add_response(
            json={"copyright": "...", "records": []},
        )
        result = client.get_standings(season=2025)
        assert result.ok
        assert "records" in result.data


class TestMLBClientTransactions:
    def test_get_transactions(self, httpx_mock: HTTPXMock, client: MLBClient):
        httpx_mock.add_response(
            json={"copyright": "...", "transactions": []},
        )
        result = client.get_transactions(start_date="2025-04-01", end_date="2025-04-07")
        assert result.ok
