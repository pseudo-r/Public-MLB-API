"""DRF ViewSets for MLB data."""

from django.db.models import Q, QuerySet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.mlb.filters import GameFilter, PlayerFilter, StandingFilter, TransactionFilter
from apps.mlb.models import Game, Player, Standing, Team, Transaction, Venue
from apps.mlb.serializers import (
    GameListSerializer,
    GameSerializer,
    PlayerListSerializer,
    PlayerSerializer,
    StandingSerializer,
    TeamListSerializer,
    TeamSerializer,
    TransactionSerializer,
    VenueSerializer,
)


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    """MLB stadiums and venue data."""

    serializer_class = VenueSerializer
    search_fields = ["name", "city", "state"]
    ordering_fields = ["name", "capacity"]
    ordering = ["name"]

    def get_queryset(self) -> QuerySet[Venue]:
        qs = Venue.objects.all()
        if self.request.query_params.get("active"):
            qs = qs.filter(active=True)
        return qs

    @extend_schema(tags=["Venues"], summary="List MLB venues")
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Venues"], summary="Get venue details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """MLB team data."""

    search_fields = ["name", "abbreviation", "location_name", "team_name"]
    ordering_fields = ["name", "abbreviation"]
    ordering = ["name"]

    def get_queryset(self) -> QuerySet[Team]:
        qs = Team.objects.select_related("venue").filter(sport_id=1)
        if not self.request.query_params.get("include_inactive"):
            qs = qs.filter(active=True)
        league_id = self.request.query_params.get("league_id")
        if league_id and league_id.isdigit():
            qs = qs.filter(league_id=league_id)
        division_id = self.request.query_params.get("division_id")
        if division_id and division_id.isdigit():
            qs = qs.filter(division_id=division_id)
        return qs

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return TeamListSerializer
        return TeamSerializer

    @extend_schema(
        tags=["Teams"],
        summary="List MLB teams",
        parameters=[
            OpenApiParameter("league_id", description="Filter by league (103=AL, 104=NL)", type=int),
            OpenApiParameter("division_id", description="Filter by division ID", type=int),
            OpenApiParameter("include_inactive", description="Include inactive/historical teams", type=bool),
            OpenApiParameter("search", description="Search by name / abbreviation", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Teams"], summary="Get team details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Teams"],
        summary="Get team by MLB ID",
        parameters=[OpenApiParameter("mlb_id", location=OpenApiParameter.PATH, type=int)],
    )
    @action(detail=False, methods=["get"], url_path="mlb/(?P<mlb_id>[0-9]+)")
    def by_mlb_id(self, request: Request, mlb_id: str) -> Response:  # noqa: ARG002
        team = self.get_queryset().filter(mlb_id=mlb_id).first()
        if not team:
            return Response({"error": "Team not found"}, status=404)
        return Response(TeamSerializer(team).data)


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """MLB player profiles."""

    filterset_class = PlayerFilter
    search_fields = ["full_name", "last_name", "primary_number"]
    ordering_fields = ["last_name", "full_name", "created_at"]
    ordering = ["last_name"]

    def get_queryset(self) -> QuerySet[Player]:
        return Player.objects.select_related("team")

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return PlayerListSerializer
        return PlayerSerializer

    @extend_schema(
        tags=["Players"],
        summary="List MLB players",
        parameters=[
            OpenApiParameter("team", description="Filter by team abbreviation or MLB ID", type=str),
            OpenApiParameter("position", description="Filter by position abbreviation (e.g., SP, C)", type=str),
            OpenApiParameter("active", description="Filter by active status", type=bool),
            OpenApiParameter("search", description="Search by name or jersey number", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Players"], summary="Get player details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Players"],
        summary="Get player by MLB ID",
        parameters=[OpenApiParameter("mlb_id", location=OpenApiParameter.PATH, type=int)],
    )
    @action(detail=False, methods=["get"], url_path="mlb/(?P<mlb_id>[0-9]+)")
    def by_mlb_id(self, request: Request, mlb_id: str) -> Response:  # noqa: ARG002
        player = self.get_queryset().filter(mlb_id=mlb_id).first()
        if not player:
            return Response({"error": "Player not found"}, status=404)
        return Response(PlayerSerializer(player).data)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """MLB game data."""

    filterset_class = GameFilter
    search_fields = ["home_team__name", "away_team__name", "home_team__abbreviation", "away_team__abbreviation"]
    ordering_fields = ["game_date", "season"]
    ordering = ["-game_date"]

    def get_queryset(self) -> QuerySet[Game]:
        return Game.objects.select_related(
            "home_team", "away_team", "venue"
        )

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return GameListSerializer
        return GameSerializer

    @extend_schema(
        tags=["Games"],
        summary="List MLB games",
        parameters=[
            OpenApiParameter("date", description="Filter by date (YYYY-MM-DD)", type=str),
            OpenApiParameter("date_from", description="Games on or after date", type=str),
            OpenApiParameter("date_to", description="Games on or before date", type=str),
            OpenApiParameter("season", description="Filter by season year", type=int),
            OpenApiParameter("team", description="Filter by team abbreviation or MLB ID", type=str),
            OpenApiParameter("status", description="Filter by game status", type=str),
            OpenApiParameter("game_type", description="Filter by game type (R, S, W, etc.)", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Games"], summary="Get game details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Games"],
        summary="Get game by MLB game PK",
        parameters=[OpenApiParameter("mlb_pk", location=OpenApiParameter.PATH, type=int)],
    )
    @action(detail=False, methods=["get"], url_path="mlb/(?P<mlb_pk>[0-9]+)")
    def by_mlb_pk(self, request: Request, mlb_pk: str) -> Response:  # noqa: ARG002
        game = self.get_queryset().filter(mlb_pk=mlb_pk).first()
        if not game:
            return Response({"error": "Game not found"}, status=404)
        return Response(GameSerializer(game).data)


class StandingViewSet(viewsets.ReadOnlyModelViewSet):
    """MLB division standings."""

    serializer_class = StandingSerializer
    filterset_class = StandingFilter
    ordering_fields = ["division_rank", "wins", "league_rank"]
    ordering = ["division_rank"]

    def get_queryset(self) -> QuerySet[Standing]:
        return Standing.objects.select_related("team")

    @extend_schema(
        tags=["Standings"],
        summary="List standings",
        parameters=[
            OpenApiParameter("season", description="Filter by season year", type=int),
            OpenApiParameter("league_id", description="103=AL, 104=NL", type=int),
            OpenApiParameter("division_id", description="Division ID", type=int),
            OpenApiParameter(
                "standings_type",
                description="regularSeason, springTraining, firstHalf, secondHalf, playoffs",
                type=str,
            ),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Standings"], summary="Get standing detail")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """MLB player transactions."""

    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    search_fields = ["person_name", "description", "type_desc"]
    ordering_fields = ["date", "created_at"]
    ordering = ["-date"]

    def get_queryset(self) -> QuerySet[Transaction]:
        return Transaction.objects.select_related("to_team", "from_team")

    @extend_schema(
        tags=["Transactions"],
        summary="List player transactions",
        parameters=[
            OpenApiParameter("date_from", description="Transactions on or after (YYYY-MM-DD)", type=str),
            OpenApiParameter("date_to", description="Transactions on or before (YYYY-MM-DD)", type=str),
            OpenApiParameter("type_code", description="Transaction type code (e.g., TR, SG, DFA)", type=str),
            OpenApiParameter("team", description="Filter by team abbreviation or MLB ID", type=str),
            OpenApiParameter("search", description="Search player name / description", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Transactions"], summary="Get transaction details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)
