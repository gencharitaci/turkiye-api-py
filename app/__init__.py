"""
Turkiye API - Comprehensive REST API and Python SDK for Turkiye's administrative divisions.

This package provides:
1. A FastAPI-based REST API server for Turkiye's administrative data
2. A Python SDK client for programmatic access to the API

Usage as Server:
    $ turkiye-api serve
    $ turkiye-api serve --reload  # Development mode
    $ turkiye-api serve --workers 4  # Production mode

Usage as SDK:
    >>> from app import TurkiyeClient
    >>> client = TurkiyeClient()
    >>> provinces = client.get_provinces()
    >>> istanbul = client.get_province(34)
"""

__version__ = "1.1.1"
__author__ = "Adem Kurtipek"
__email__ = "gncharitaci@gmail.com"
__license__ = "MIT"

# Export main client class
from app.client import TurkiyeAPIError, TurkiyeClient

__all__ = [
    "TurkiyeClient",
    "TurkiyeAPIError",
    "__version__",
]
