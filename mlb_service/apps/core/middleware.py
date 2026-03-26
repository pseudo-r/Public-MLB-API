"""Core middleware for request handling."""

import time
import uuid
from collections.abc import Callable

import structlog
from django.http import HttpRequest, HttpResponse

logger = structlog.get_logger(__name__)


class RequestIDMiddleware:
    """Add unique request ID to each request for tracing."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id  # type: ignore[attr-defined]

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response


class StructuredLoggingMiddleware:
    """Log request/response information in a structured format."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path == "/healthz":
            return self.get_response(request)

        start_time = time.perf_counter()

        logger.info(
            "request_started",
            method=request.method,
            path=request.path,
            query_params=dict(request.GET),
            user_agent=request.headers.get("User-Agent", ""),
        )

        response = self.get_response(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "request_finished",
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        return response
