"""URL routing for ingest trigger endpoints."""

from django.urls import path

from apps.ingest.views import (
    IngestScheduleView,
    IngestStandingsView,
    IngestTeamsView,
    IngestTransactionsView,
)

urlpatterns = [
    path("teams/", IngestTeamsView.as_view(), name="ingest-teams"),
    path("schedule/", IngestScheduleView.as_view(), name="ingest-schedule"),
    path("standings/", IngestStandingsView.as_view(), name="ingest-standings"),
    path("transactions/", IngestTransactionsView.as_view(), name="ingest-transactions"),
]
