"""django-filter FilterSets for MLB models."""

import django_filters

from apps.mlb.models import Game, Player, Standing, Transaction


class GameFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="official_date")
    date_from = django_filters.DateFilter(field_name="official_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="official_date", lookup_expr="lte")
    season = django_filters.NumberFilter(field_name="season")
    team = django_filters.CharFilter(method="filter_team")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    game_type = django_filters.CharFilter(field_name="game_type", lookup_expr="iexact")

    class Meta:
        model = Game
        fields = ["date", "date_from", "date_to", "season", "status", "game_type"]

    def filter_team(self, queryset, name, value):  # noqa: ARG002
        """Filter by team ID or abbreviation (home or away)."""
        if value.isdigit():
            return queryset.filter(
                home_team__mlb_id=value
            ) | queryset.filter(away_team__mlb_id=value)
        return queryset.filter(
            home_team__abbreviation__iexact=value
        ) | queryset.filter(away_team__abbreviation__iexact=value)


class PlayerFilter(django_filters.FilterSet):
    team = django_filters.CharFilter(method="filter_team")
    position = django_filters.CharFilter(
        field_name="position_abbreviation", lookup_expr="iexact"
    )
    active = django_filters.BooleanFilter(field_name="active")

    class Meta:
        model = Player
        fields = ["active", "position"]

    def filter_team(self, queryset, name, value):  # noqa: ARG002
        if value.isdigit():
            return queryset.filter(team__mlb_id=value)
        return queryset.filter(team__abbreviation__iexact=value)


class StandingFilter(django_filters.FilterSet):
    season = django_filters.NumberFilter(field_name="season")
    league_id = django_filters.NumberFilter(field_name="league_id")
    division_id = django_filters.NumberFilter(field_name="division_id")
    standings_type = django_filters.CharFilter(field_name="standings_type", lookup_expr="iexact")

    class Meta:
        model = Standing
        fields = ["season", "league_id", "division_id", "standings_type"]


class TransactionFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    type_code = django_filters.CharFilter(field_name="type_code", lookup_expr="iexact")
    team = django_filters.CharFilter(method="filter_team")

    class Meta:
        model = Transaction
        fields = ["date_from", "date_to", "type_code"]

    def filter_team(self, queryset, name, value):  # noqa: ARG002
        if value.isdigit():
            return queryset.filter(
                to_team__mlb_id=value
            ) | queryset.filter(from_team__mlb_id=value)
        return queryset.filter(
            to_team__abbreviation__iexact=value
        ) | queryset.filter(from_team__abbreviation__iexact=value)
