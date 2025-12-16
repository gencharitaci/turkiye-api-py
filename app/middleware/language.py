"""
Language Detection Middleware
Enterprise-level language detection and persistence
"""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.i18n import (
    DEFAULT_LANGUAGE,
    extract_language_from_path,
    is_valid_language,
    negotiate_language,
    normalize_language_code,
    set_current_language,
)

logger = logging.getLogger(__name__)


class LanguageMiddleware(BaseHTTPMiddleware):
    """
    Middleware for automatic language detection and persistence

    Detection Priority:
    1. URL path (e.g., /docs/en)
    2. Cookie (language preference)
    3. X-Language header (custom header)
    4. Accept-Language header (browser preference)
    5. Default language
    """

    def __init__(
        self,
        app,
        cookie_name: str = "language",
        cookie_max_age: int = 31536000,  # 1 year
        cookie_path: str = "/",
        cookie_secure: bool = False,
        cookie_httponly: bool = False,
        cookie_samesite: str = "lax",
    ):
        """
        Initialize language middleware

        Args:
            app: FastAPI application
            cookie_name: Name of the language cookie
            cookie_max_age: Cookie expiration time in seconds (default: 1 year)
            cookie_path: Cookie path
            cookie_secure: Whether cookie requires HTTPS
            cookie_httponly: Whether cookie is HTTP only
            cookie_samesite: SameSite cookie attribute
        """
        super().__init__(app)
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.cookie_path = cookie_path
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        self.cookie_samesite = cookie_samesite

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and detect language

        Args:
            request: Incoming request
            call_next: Next middleware/handler

        Returns:
            Response with language cookie set if needed
        """
        # Detect language from multiple sources
        language = self.detect_language_from_sources(request)

        # Set language in context for this request
        set_current_language(language)

        # Store language in request state for easy access
        request.state.language = language

        # Process request
        response = await call_next(request)

        # Check if we need to set/update the cookie
        cookie_language = request.cookies.get(self.cookie_name)

        # Set cookie if:
        # 1. No cookie exists
        # 2. Cookie value differs from detected language
        # 3. Language was explicitly set via URL or header
        if cookie_language != language:
            self.set_language_cookie(response, language)
            logger.debug(f"Set language cookie: {language}")

        return response

    def detect_language_from_sources(self, request: Request) -> str:
        """
        Detect language from multiple sources with priority

        Priority:
        1. URL path
        2. Cookie
        3. X-Language header
        4. Accept-Language header
        5. Default

        Args:
            request: Incoming request

        Returns:
            Detected language code
        """
        # 1. Check URL path (highest priority)
        path_language = extract_language_from_path(request.url.path)
        if path_language:
            logger.debug(f"Language from URL path: {path_language}")
            return path_language

        # 2. Check cookie
        cookie_language = request.cookies.get(self.cookie_name)
        if cookie_language and is_valid_language(cookie_language):
            logger.debug(f"Language from cookie: {cookie_language}")
            return cookie_language

        # 3. Check X-Language header (custom header)
        x_language = request.headers.get("x-language", "")
        if x_language:
            normalized = normalize_language_code(x_language)
            if is_valid_language(normalized):
                logger.debug(f"Language from X-Language header: {normalized}")
                return normalized

        # 4. Check Accept-Language header (browser preference)
        accept_language = request.headers.get("accept-language", "")
        if accept_language:
            negotiated = negotiate_language(accept_language)
            if negotiated != DEFAULT_LANGUAGE:
                logger.debug(f"Language from Accept-Language: {negotiated}")
                return negotiated

        # 5. Default language
        logger.debug(f"Using default language: {DEFAULT_LANGUAGE}")
        return DEFAULT_LANGUAGE

    def set_language_cookie(self, response: Response, language: str) -> None:
        """
        Set language cookie in response

        Args:
            response: Response object
            language: Language code to set
        """
        response.set_cookie(
            key=self.cookie_name,
            value=language,
            max_age=self.cookie_max_age,
            path=self.cookie_path,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )


def get_request_language(request: Request) -> str:
    """
    Get language for current request

    This is a helper function to get language from request state
    Falls back to context if not in request state

    Args:
        request: Current request

    Returns:
        Language code
    """
    from app.i18n import get_current_language

    # Try to get from request state first
    if hasattr(request.state, "language"):
        return request.state.language

    # Fallback to context
    return get_current_language()
