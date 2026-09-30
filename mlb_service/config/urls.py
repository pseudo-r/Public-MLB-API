"""URL configuration for mlb_service."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.core.upstream import UpstreamView
from apps.core.views import HealthCheckView

urlpatterns = [
    path("api/v1/live/teams/<int:team_id>/roster/", UpstreamView.as_view(client_method="get_team_roster"), name="live-get_team_roster"),
    path("api/v1/live/games/<int:game_pk>/plays/", UpstreamView.as_view(client_method="get_game_play_by_play"), name="live-get_game_play_by_play"),
    path("api/v1/live/divisions/", UpstreamView.as_view(client_method="get_divisions"), name="live-get_divisions"),


    # Admin
    path("admin/", admin.site.urls),
    # Health check
    path("healthz", HealthCheckView.as_view(), name="health-check"),
    # API v1
    path("api/v1/", include("apps.mlb.urls")),
    path("api/v1/ingest/", include("apps.ingest.urls")),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
