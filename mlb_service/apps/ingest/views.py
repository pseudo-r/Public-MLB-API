"""Trigger views for ingest endpoints."""

from datetime import date

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class IngestTeamsView(APIView):
    """Trigger MLB team + venue ingestion."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest MLB teams",
        description="Fetches all active MLB teams (and venues) from statsapi.mlb.com and upserts to DB.",
        responses={200: {"type": "object"}},
    )
    def post(self, request: Request) -> Response:  # noqa: ARG002
        from apps.ingest.services import TeamIngestionService, VenueIngestionService

        venue_result = VenueIngestionService().ingest_venues()
        team_result = TeamIngestionService().ingest_teams()
        return Response({"venues": venue_result.to_dict(), "teams": team_result.to_dict()})


class IngestScheduleView(APIView):
    """Trigger MLB schedule ingestion for a date."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest MLB schedule",
        description="Fetches and upserts MLB games for a date (defaults to today). Body: `{\"date\": \"YYYY-MM-DD\"}`.",
        responses={200: {"type": "object"}},
    )
    def post(self, request: Request) -> Response:
        date_str = request.data.get("date") or date.today().isoformat()
        from apps.ingest.services import ScheduleIngestionService

        result = ScheduleIngestionService().ingest_schedule(date_str=date_str)
        return Response({"date": date_str, **result.to_dict()})


class IngestStandingsView(APIView):
    """Trigger MLB standings ingestion."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest MLB standings",
        description="Fetches and upserts division standings. Body: `{\"season\": 2025}`.",
        responses={200: {"type": "object"}},
    )
    def post(self, request: Request) -> Response:
        from datetime import datetime

        season = request.data.get("season") or datetime.now().year
        standings_type = request.data.get("standings_type", "regularSeason")
        from apps.ingest.services import StandingsIngestionService

        result = StandingsIngestionService().ingest_standings(
            season=int(season), standings_type=standings_type
        )
        return Response({"season": season, **result.to_dict()})


class IngestTransactionsView(APIView):
    """Trigger MLB transaction ingestion."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest MLB transactions",
        description=(
            "Fetches and upserts player transactions for a date range. "
            "Body: `{\"start_date\": \"YYYY-MM-DD\", \"end_date\": \"YYYY-MM-DD\"}`."
        ),
        responses={200: {"type": "object"}},
    )
    def post(self, request: Request) -> Response:
        today = date.today().isoformat()
        start = request.data.get("start_date") or today
        end = request.data.get("end_date") or today
        from apps.ingest.services import TransactionIngestionService

        result = TransactionIngestionService().ingest_transactions(
            start_date=start, end_date=end
        )
        return Response({"start_date": start, "end_date": end, **result.to_dict()})
