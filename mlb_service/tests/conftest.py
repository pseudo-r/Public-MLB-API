"""Test fixtures for mlb_service tests."""

from __future__ import annotations

import pytest
from django.test import TestCase

from apps.mlb.models import Game, Player, Standing, Team, Transaction, Venue


@pytest.fixture
def venue(db):
    return Venue.objects.create(
        mlb_id=22,
        name="Dodger Stadium",
        city="Los Angeles",
        state="CA",
        capacity=56000,
        roof_type="Open",
        turf_type="Grass",
    )


@pytest.fixture
def team_dodgers(db, venue):
    return Team.objects.create(
        mlb_id=119,
        name="Los Angeles Dodgers",
        team_name="Dodgers",
        location_name="Los Angeles",
        abbreviation="LAD",
        team_code="lan",
        league_id=104,
        league_name="National League",
        division_id=203,
        division_name="NL West",
        venue=venue,
        active=True,
    )


@pytest.fixture
def team_yankees(db):
    return Team.objects.create(
        mlb_id=147,
        name="New York Yankees",
        team_name="Yankees",
        location_name="New York",
        abbreviation="NYY",
        team_code="nya",
        league_id=103,
        league_name="American League",
        division_id=201,
        division_name="AL East",
        active=True,
    )


@pytest.fixture
def player(db, team_dodgers):
    return Player.objects.create(
        mlb_id=660271,
        full_name="Shohei Ohtani",
        first_name="Shohei",
        last_name="Ohtani",
        primary_number="17",
        position="Designated Hitter",
        position_abbreviation="DH",
        bat_side="L",
        pitch_hand="R",
        team=team_dodgers,
        active=True,
    )


@pytest.fixture
def game(db, team_dodgers, team_yankees, venue):
    from datetime import datetime, timezone

    return Game.objects.create(
        mlb_pk=745444,
        game_date=datetime(2025, 4, 1, 22, 10, tzinfo=timezone.utc),
        official_date="2025-04-01",
        game_type="R",
        season=2025,
        home_team=team_dodgers,
        away_team=team_yankees,
        venue=venue,
        status=Game.STATUS_FINAL,
        home_score=5,
        away_score=3,
    )


@pytest.fixture
def standing(db, team_dodgers):
    return Standing.objects.create(
        team=team_dodgers,
        season=2025,
        standings_type="regularSeason",
        league_id=104,
        division_id=203,
        division_rank=1,
        wins=10,
        losses=2,
        pct=".833",
    )
