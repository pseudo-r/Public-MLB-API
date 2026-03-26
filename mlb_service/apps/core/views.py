"""Health check view."""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Simple liveness probe — returns 200 if the app is running."""

    authentication_classes = []
    permission_classes = []

    def get(self, request: Request) -> Response:  # noqa: ARG002
        return Response({"status": "ok"})
