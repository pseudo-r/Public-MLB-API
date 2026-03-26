"""Serializers for MLB data models."""

from rest_framework import serializers

from apps.mlb.models import Game, Player, Standing, Team, Transaction, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            "id",
            "mlb_id",
            "name",
            "city",
            "state",
            "country",
            "capacity",
            "roof_type",
            "turf_type",
            "left_line",
            "left_center",
            "center",
            "right_center",
            "right_line",
            "latitude",
            "longitude",
            "active",
        ]


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "mlb_id",
            "name",
            "abbreviation",
            "league_name",
            "division_name",
            "active",
        ]


class TeamSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "mlb_id",
            "name",
            "team_name",
            "location_name",
            "abbreviation",
            "team_code",
            "file_code",
            "league_id",
            "league_name",
            "division_id",
            "division_name",
            "sport_id",
            "venue",
            "first_year_of_play",
            "active",
            "created_at",
            "updated_at",
        ]


class PlayerListSerializer(serializers.ModelSerializer):
    team_abbreviation = serializers.CharField(source="team.abbreviation", read_only=True, default=None)

    class Meta:
        model = Player
        fields = [
            "id",
            "mlb_id",
            "full_name",
            "primary_number",
            "position_abbreviation",
            "team_abbreviation",
            "active",
        ]


class PlayerSerializer(serializers.ModelSerializer):
    team = TeamListSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "mlb_id",
            "full_name",
            "first_name",
            "last_name",
            "primary_number",
            "birth_date",
            "birth_city",
            "birth_country",
            "height",
            "weight",
            "position",
            "position_abbreviation",
            "position_type",
            "bat_side",
            "pitch_hand",
            "team",
            "active",
            "mlb_debut_date",
            "last_played_date",
            "headshot_url",
            "created_at",
            "updated_at",
        ]


class GameListSerializer(serializers.ModelSerializer):
    home_team = TeamListSerializer(read_only=True)
    away_team = TeamListSerializer(read_only=True)
    final_score = serializers.CharField(read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "mlb_pk",
            "game_date",
            "official_date",
            "game_type",
            "season",
            "home_team",
            "away_team",
            "status",
            "home_score",
            "away_score",
            "final_score",
        ]


class GameSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    final_score = serializers.CharField(read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "mlb_pk",
            "game_date",
            "official_date",
            "game_type",
            "season",
            "series_description",
            "home_team",
            "away_team",
            "venue",
            "status",
            "detailed_state",
            "home_score",
            "away_score",
            "final_score",
            "current_inning",
            "inning_state",
            "double_header",
            "game_number",
            "created_at",
            "updated_at",
        ]


class StandingSerializer(serializers.ModelSerializer):
    team = TeamListSerializer(read_only=True)

    class Meta:
        model = Standing
        fields = [
            "id",
            "team",
            "season",
            "standings_type",
            "league_id",
            "division_id",
            "division_rank",
            "league_rank",
            "wild_card_rank",
            "wins",
            "losses",
            "pct",
            "games_back",
            "wild_card_games_back",
            "streak_code",
            "last_ten",
            "clinched",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    to_team = TeamListSerializer(read_only=True)
    from_team = TeamListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "mlb_id",
            "person_name",
            "person_mlb_id",
            "to_team",
            "from_team",
            "date",
            "effective_date",
            "type_code",
            "type_desc",
            "description",
            "created_at",
            "updated_at",
        ]
