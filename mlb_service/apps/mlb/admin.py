"""Django admin for MLB models."""

from django.contrib import admin

from apps.mlb.models import Game, Player, Standing, Team, Transaction, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "state", "capacity", "roof_type", "turf_type", "active"]
    list_filter = ["active", "roof_type", "turf_type"]
    search_fields = ["name", "city", "state"]
    readonly_fields = ["mlb_id", "created_at", "updated_at"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "abbreviation", "league_name", "division_name", "active"]
    list_filter = ["active", "league_id", "division_id"]
    search_fields = ["name", "abbreviation", "team_code"]
    readonly_fields = ["mlb_id", "created_at", "updated_at"]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "primary_number",
        "position_abbreviation",
        "team",
        "bat_side",
        "pitch_hand",
        "active",
    ]
    list_filter = ["active", "position_abbreviation", "bat_side", "pitch_hand"]
    search_fields = ["full_name", "last_name", "first_name"]
    raw_id_fields = ["team"]
    readonly_fields = ["mlb_id", "created_at", "updated_at"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "game_date",
        "season",
        "game_type",
        "status",
        "home_score",
        "away_score",
    ]
    list_filter = ["status", "game_type", "season"]
    search_fields = ["home_team__name", "away_team__name", "home_team__abbreviation"]
    date_hierarchy = "game_date"
    raw_id_fields = ["home_team", "away_team", "venue"]
    readonly_fields = ["mlb_pk", "created_at", "updated_at"]


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = [
        "team",
        "season",
        "division_rank",
        "wins",
        "losses",
        "pct",
        "games_back",
        "clinched",
    ]
    list_filter = ["season", "standings_type", "league_id", "division_id"]
    raw_id_fields = ["team"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["person_name", "type_desc", "to_team", "from_team", "date"]
    list_filter = ["type_code", "date"]
    search_fields = ["person_name", "description", "type_desc"]
    date_hierarchy = "date"
    raw_id_fields = ["to_team", "from_team"]
    readonly_fields = ["mlb_id", "created_at", "updated_at"]
