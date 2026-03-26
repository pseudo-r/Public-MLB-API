"""API endpoint tests."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_returns_ok(self, api_client):
        response = api_client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


@pytest.mark.django_db
class TestTeamAPI:
    def test_list_teams_empty(self, api_client):
        response = api_client.get("/api/v1/teams/")
        assert response.status_code == 200
        assert response.json()["count"] == 0

    def test_list_teams(self, api_client, team_dodgers):
        response = api_client.get("/api/v1/teams/")
        assert response.status_code == 200
        assert response.json()["count"] == 1
        assert response.json()["results"][0]["abbreviation"] == "LAD"

    def test_retrieve_team(self, api_client, team_dodgers):
        response = api_client.get(f"/api/v1/teams/{team_dodgers.pk}/")
        assert response.status_code == 200
        assert response.json()["mlb_id"] == 119

    def test_team_by_mlb_id(self, api_client, team_dodgers):
        response = api_client.get("/api/v1/teams/mlb/119/")
        assert response.status_code == 200
        assert response.json()["abbreviation"] == "LAD"

    def test_filter_by_league_id(self, api_client, team_dodgers, team_yankees):
        response = api_client.get("/api/v1/teams/?league_id=104")
        assert response.status_code == 200
        assert response.json()["count"] == 1
        assert response.json()["results"][0]["abbreviation"] == "LAD"


@pytest.mark.django_db
class TestPlayerAPI:
    def test_list_players(self, api_client, player):
        response = api_client.get("/api/v1/players/")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_player_by_mlb_id(self, api_client, player):
        response = api_client.get("/api/v1/players/mlb/660271/")
        assert response.status_code == 200
        assert response.json()["full_name"] == "Shohei Ohtani"

    def test_filter_by_position(self, api_client, player):
        response = api_client.get("/api/v1/players/?position=DH")
        assert response.status_code == 200
        assert response.json()["count"] == 1


@pytest.mark.django_db
class TestGameAPI:
    def test_list_games(self, api_client, game):
        response = api_client.get("/api/v1/games/")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_retrieve_game(self, api_client, game):
        response = api_client.get(f"/api/v1/games/{game.pk}/")
        assert response.status_code == 200
        assert response.json()["mlb_pk"] == 745444

    def test_game_by_mlb_pk(self, api_client, game):
        response = api_client.get("/api/v1/games/mlb/745444/")
        assert response.status_code == 200

    def test_filter_by_date(self, api_client, game):
        response = api_client.get("/api/v1/games/?date=2025-04-01")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_filter_by_team_abbreviation(self, api_client, game):
        response = api_client.get("/api/v1/games/?team=LAD")
        assert response.status_code == 200
        assert response.json()["count"] == 1


@pytest.mark.django_db
class TestStandingAPI:
    def test_list_standings(self, api_client, standing):
        response = api_client.get("/api/v1/standings/")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_filter_by_season(self, api_client, standing):
        response = api_client.get("/api/v1/standings/?season=2025")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_filter_by_wrong_season(self, api_client, standing):
        response = api_client.get("/api/v1/standings/?season=2020")
        assert response.status_code == 200
        assert response.json()["count"] == 0


@pytest.mark.django_db
class TestVenueAPI:
    def test_list_venues(self, api_client, venue):
        response = api_client.get("/api/v1/venues/")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_retrieve_venue(self, api_client, venue):
        response = api_client.get(f"/api/v1/venues/{venue.pk}/")
        assert response.status_code == 200
        assert response.json()["mlb_id"] == 22
