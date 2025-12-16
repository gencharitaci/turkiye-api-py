"""
API versioning strategy and utilities.

This module provides infrastructure for API versioning to support multiple
API versions simultaneously and enable smooth migration paths for clients.
"""

import logging
from enum import Enum
from typing import Optional

from fastapi import Header, HTTPException, Request

logger = logging.getLogger(__name__)


class APIVersion(str, Enum):
    """Supported API versions."""

    V1 = "v1"
    V2 = "v2"  # Future version placeholder


# Current default and latest versions
DEFAULT_VERSION = APIVersion.V1
LATEST_VERSION = APIVersion.V1
SUPPORTED_VERSIONS = [APIVersion.V1]


def get_api_version_from_path(request: Request) -> Optional[str]:
    """
    Extract API version from request path.

    Args:
        request: FastAPI request object

    Returns:
        API version string (e.g., "v1") or None if not found
    """
    path = request.url.path
    parts = path.split("/")

    # Look for version pattern (v1, v2, etc.)
    for part in parts:
        if part.startswith("v") and part[1:].isdigit():
            return part

    return None


def get_api_version(
    request: Request, x_api_version: Optional[str] = Header(None, description="API version override")
) -> str:
    """
    Determine API version for the request using multiple strategies.

    Priority order:
    1. X-API-Version header
    2. URL path segment (e.g., /api/v1/...)
    3. Default version

    Args:
        request: FastAPI request object
        x_api_version: Optional API version from header

    Returns:
        API version string (e.g., "v1")

    Raises:
        HTTPException: If requested version is not supported
    """
    # Strategy 1: Check header
    if x_api_version:
        version = x_api_version.lower()
        if version not in [v.value for v in SUPPORTED_VERSIONS]:
            supported = [v.value for v in SUPPORTED_VERSIONS]
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported API version: {version}. Supported versions: {supported}",
            )
        logger.debug(f"API version from header: {version}")
        return version

    # Strategy 2: Check URL path
    path_version = get_api_version_from_path(request)
    if path_version:
        if path_version not in [v.value for v in SUPPORTED_VERSIONS]:
            supported = [v.value for v in SUPPORTED_VERSIONS]
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported API version in path: {path_version}. Supported versions: {supported}",
            )
        logger.debug(f"API version from path: {path_version}")
        return path_version

    # Strategy 3: Use default
    logger.debug(f"Using default API version: {DEFAULT_VERSION.value}")
    return DEFAULT_VERSION.value


def is_version_deprecated(version: str) -> bool:
    """
    Check if an API version is deprecated.

    Args:
        version: API version string

    Returns:
        True if version is deprecated, False otherwise
    """
    # Currently no deprecated versions
    # Example for future:
    # return version in ["v0", "v1"]
    return False


def get_deprecation_info(version: str) -> Optional[dict]:
    """
    Get deprecation information for an API version.

    Args:
        version: API version string

    Returns:
        Dictionary with deprecation details or None if not deprecated
    """
    if not is_version_deprecated(version):
        return None

    # Example deprecation info structure
    deprecation_map = {
        # "v1": {
        #     "deprecated": True,
        #     "sunset_date": "2026-12-31",
        #     "migration_guide": "https://docs.example.com/migration/v1-to-v2",
        #     "alternative_version": "v2"
        # }
    }

    return deprecation_map.get(version)


def add_version_headers(version: str, headers: dict) -> dict:
    """
    Add version-related headers to API response.

    Args:
        version: Current API version
        headers: Existing response headers

    Returns:
        Updated headers dictionary
    """
    headers["X-API-Version"] = version
    headers["X-API-Latest-Version"] = LATEST_VERSION.value

    # Add deprecation warning if applicable
    deprecation_info = get_deprecation_info(version)
    if deprecation_info:
        headers["X-API-Deprecated"] = "true"
        if "sunset_date" in deprecation_info:
            headers["X-API-Sunset-Date"] = deprecation_info["sunset_date"]
        if "alternative_version" in deprecation_info:
            headers["X-API-Alternative-Version"] = deprecation_info["alternative_version"]

    return headers


class VersionedResponse:
    """
    Helper class for creating version-aware API responses.

    This can be used to customize responses based on API version.
    """

    @staticmethod
    def format_response(data: dict, version: str) -> dict:
        """
        Format response data based on API version.

        Args:
            data: Response data
            version: API version

        Returns:
            Formatted response data
        """
        # V1 format (current)
        if version == APIVersion.V1.value:
            return data

        # V2 format (future - example structure)
        # if version == APIVersion.V2.value:
        #     return {
        #         "data": data,
        #         "meta": {
        #             "version": version,
        #             "timestamp": datetime.utcnow().isoformat()
        #         }
        #     }

        # Default: return as-is
        return data


def get_version_info() -> dict:
    """
    Get information about all supported API versions.

    Returns:
        Dictionary containing version information
    """
    versions = []

    for version in SUPPORTED_VERSIONS:
        version_info = {
            "version": version.value,
            "status": "current" if version == LATEST_VERSION else "supported",
            "deprecated": is_version_deprecated(version.value),
        }

        # Add deprecation details if applicable
        deprecation_info = get_deprecation_info(version.value)
        if deprecation_info:
            version_info.update(deprecation_info)

        versions.append(version_info)

    return {
        "current_version": LATEST_VERSION.value,
        "default_version": DEFAULT_VERSION.value,
        "supported_versions": versions,
    }
