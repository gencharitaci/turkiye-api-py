"""
Request metrics and monitoring middleware.

This middleware tracks request duration, status codes, and other metrics
for observability and performance monitoring.
"""

import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for collecting request metrics and performance data.

    Tracks:
    - Request duration (in milliseconds)
    - HTTP method and path
    - Status code
    - Client IP address
    - User agent

    Adds X-Response-Time header to all responses.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process request and collect metrics.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            Response with added metrics headers
        """
        # Record start time
        start_time = time.time()

        # Extract request metadata
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        # Process request
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # Log error and re-raise
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                "Request failed",
                extra={
                    "method": method,
                    "path": path,
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": client_ip,
                    "error": str(e),
                },
            )
            raise

        # Calculate request duration
        duration_ms = (time.time() - start_time) * 1000

        # Log request metrics (structured logging)
        logger.info(
            "Request completed",
            extra={
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": round(duration_ms, 2),
                "client_ip": client_ip,
                "user_agent": user_agent,
            },
        )

        # Add response time header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

        # Note: X-Powered-By header removed for security
        # Now handled by SecurityHeadersMiddleware (configurable via settings)

        return response


class RequestCountMiddleware(BaseHTTPMiddleware):
    """
    Simple request counter middleware.

    Tracks total number of requests processed.
    Useful for basic monitoring and health checks.
    """

    def __init__(self, app):
        super().__init__(app)
        self.request_count = 0

    async def dispatch(self, request: Request, call_next):
        """
        Increment request counter and process request.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            Response from next handler
        """
        self.request_count += 1
        response = await call_next(request)

        # Add request count header for debugging
        response.headers["X-Request-Count"] = str(self.request_count)

        return response
