"""
Rate limiting middleware for API protection.

This module provides rate limiting functionality to prevent API abuse
and ensure fair usage across all clients.
"""

import logging

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)


def get_identifier(request) -> str:
    """
    Get client identifier for rate limiting.

    Uses the following priority:
    1. X-Forwarded-For header (for proxied requests)
    2. X-Real-IP header (for nginx proxied requests)
    3. Client IP address

    Args:
        request: FastAPI request object

    Returns:
        Client identifier string
    """
    # Check for forwarded IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can contain multiple IPs, use the first one
        return forwarded.split(",")[0].strip()

    # Check for real IP (nginx)
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fall back to direct client IP
    return get_remote_address(request)


# Create limiter instance (will be configured during setup)
limiter = None


def setup_rate_limiting(
    app,
    enabled: bool = True,
    limit_per_minute: int = 60,
    storage: str = "memory",
    redis_url: str = "redis://localhost:6379",
):
    """
    Configure rate limiting for the FastAPI application with Redis or in-memory storage.

    Args:
        app: FastAPI application instance
        enabled: Whether to enable rate limiting
        limit_per_minute: Number of requests allowed per minute
        storage: Storage backend ("memory" or "redis")
        redis_url: Redis connection URL (only used if storage="redis")

    Returns:
        Configured limiter instance or None if disabled
    """
    global limiter

    if not enabled:
        logger.info("Rate limiting is disabled")
        return None

    # Determine storage URI
    if storage == "redis":
        storage_uri = redis_url
        logger.info(f"Rate limiting using Redis storage: {redis_url}")
    else:
        storage_uri = "memory://"
        logger.info("Rate limiting using in-memory storage")

    # Create limiter with appropriate storage
    limiter = Limiter(
        key_func=get_identifier,
        default_limits=[f"{limit_per_minute}/minute"],
        storage_uri=storage_uri,
        strategy="fixed-window",  # Rate limit strategy
        headers_enabled=True,  # Add rate limit headers to responses
    )

    # Add rate limit exceeded handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add SlowAPI middleware
    app.add_middleware(SlowAPIMiddleware)

    logger.info(f"Rate limiting enabled: {limit_per_minute} requests/minute")
    return limiter
