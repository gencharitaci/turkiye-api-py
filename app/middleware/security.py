"""
Security headers middleware for OWASP compliance.

This middleware adds essential security headers to all responses to protect
against common web vulnerabilities including XSS, clickjacking, and MIME sniffing.
"""

import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.settings import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses.

    Implements OWASP recommended headers for web security:
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-Frame-Options: Prevents clickjacking attacks
    - X-XSS-Protection: XSS filter (legacy but still recommended)
    - Content-Security-Policy: Controls resource loading
    - Referrer-Policy: Controls referrer information
    - Permissions-Policy: Controls browser features
    """

    def __init__(self, app, expose_server_header: bool = False):
        """
        Initialize security headers middleware.

        Args:
            app: FastAPI application instance
            expose_server_header: Whether to add X-Powered-By header (default: False for security)
        """
        super().__init__(app)
        self.expose_server_header = expose_server_header
        logger.info(f"SecurityHeadersMiddleware initialized (expose_server_header={expose_server_header})")

    async def dispatch(self, request: Request, call_next):
        """
        Process request and add security headers to response.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            Response with added security headers
        """
        response = await call_next(request)

        # Prevent MIME type sniffing (stops browsers from interpreting files as different MIME types)
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking (stops page from being loaded in frame/iframe)
        response.headers["X-Frame-Options"] = "DENY"

        # XSS protection (legacy, but still recommended for older browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy - allows only specific sources
        # Configured to allow Scalar documentation CDN
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self';"
        )

        # Referrer policy - controls what information is sent in Referer header
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions policy - disables unnecessary browser features
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Strict Transport Security - force HTTPS (only in production with HTTPS)
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Optional: X-Powered-By header (disabled by default for security)
        if self.expose_server_header:
            response.headers["X-Powered-By"] = "Turkiye-API"

        return response
