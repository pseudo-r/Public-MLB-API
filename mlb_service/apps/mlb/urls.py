"""URL routing for apps.mlb — DRF router."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.mlb.views import (
    GameViewSet,
    PlayerViewSet,
    StandingViewSet,
    TeamViewSet,
    TransactionViewSet,
    VenueViewSet,
)

router = DefaultRouter()
router.register("teams", TeamViewSet, basename="team")
router.register("players", PlayerViewSet, basename="player")
router.register("games", GameViewSet, basename="game")
router.register("standings", StandingViewSet, basename="standing")
router.register("transactions", TransactionViewSet, basename="transaction")
router.register("venues", VenueViewSet, basename="venue")

urlpatterns = [
    path("", include(router.urls)),
]
