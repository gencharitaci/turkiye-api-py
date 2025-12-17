"""
Python SDK client for Turkiye API.

This module provides a simple, Pythonic interface for interacting with
the Turkiye API programmatically.
"""

from typing import Any, Dict, List, Optional, Union

import httpx


class TurkiyeAPIError(Exception):
    """Base exception for Turkiye API client errors."""

    pass


class TurkiyeClient:
    """
    Python client for Turkiye API.

    Provides methods to query Turkiye's administrative divisions including
    provinces, districts, neighborhoods, villages, and towns.

    Example:
        >>> client = TurkiyeClient()
        >>> provinces = client.get_provinces()
        >>> istanbul = client.get_province(34)
        >>> print(istanbul['name'])
        'İstanbul'
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8181",
        timeout: float = 30.0,
        api_version: str = "v1",
        language: str = "en",
    ):
        """
        Initialize Turkiye API client.

        Args:
            base_url: Base URL of the API server
            timeout: Request timeout in seconds
            api_version: API version to use (default: v1)
            language: Preferred language for responses (en or tr)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.api_version = api_version
        self.language = language
        self.client = httpx.Client(timeout=timeout)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[Dict, List]:
        """
        Make HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            **kwargs: Additional request arguments

        Returns:
            Response data as dict or list

        Raises:
            TurkiyeAPIError: If request fails
        """
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["X-Language"] = self.language

        try:
            response = self.client.request(method, url, params=params, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise TurkiyeAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise TurkiyeAPIError(f"Request failed: {str(e)}")
        except Exception as e:
            raise TurkiyeAPIError(f"Unexpected error: {str(e)}")

    # Province Methods
    def get_provinces(
        self,
        name: Optional[str] = None,
        min_population: Optional[int] = None,
        max_population: Optional[int] = None,
        offset: int = 0,
        limit: int = 100,
        sort: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of provinces with optional filtering.

        Args:
            name: Filter by province name (partial match)
            min_population: Minimum population
            max_population: Maximum population
            offset: Pagination offset
            limit: Maximum results to return
            sort: Sort field (prefix with - for descending)
            fields: Comma-separated list of fields to return

        Returns:
            List of province dictionaries
        """
        params = {
            "name": name,
            "minPopulation": min_population,
            "maxPopulation": max_population,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "fields": fields,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "provinces", params=params)

    def get_province(self, province_id: int) -> Dict[str, Any]:
        """
        Get specific province by ID.

        Args:
            province_id: Province ID (1-81)

        Returns:
            Province dictionary
        """
        return self._request("GET", f"provinces/{province_id}")

    # District Methods
    def get_districts(
        self,
        province_id: Optional[int] = None,
        name: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
        sort: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of districts with optional filtering.

        Args:
            province_id: Filter by province ID
            name: Filter by district name (partial match)
            offset: Pagination offset
            limit: Maximum results to return
            sort: Sort field (prefix with - for descending)
            fields: Comma-separated list of fields to return

        Returns:
            List of district dictionaries
        """
        params = {
            "provinceId": province_id,
            "name": name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "fields": fields,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "districts", params=params)

    def get_district(self, district_id: int) -> Dict[str, Any]:
        """
        Get specific district by ID.

        Args:
            district_id: District ID

        Returns:
            District dictionary
        """
        return self._request("GET", f"districts/{district_id}")

    # Neighborhood Methods
    def get_neighborhoods(
        self,
        district_id: Optional[int] = None,
        name: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
        sort: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of neighborhoods with optional filtering.

        Args:
            district_id: Filter by district ID
            name: Filter by neighborhood name (partial match)
            offset: Pagination offset
            limit: Maximum results to return
            sort: Sort field (prefix with - for descending)
            fields: Comma-separated list of fields to return

        Returns:
            List of neighborhood dictionaries
        """
        params = {
            "districtId": district_id,
            "name": name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "fields": fields,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "neighborhoods", params=params)

    def get_neighborhood(self, neighborhood_id: int) -> Dict[str, Any]:
        """
        Get specific neighborhood by ID.

        Args:
            neighborhood_id: Neighborhood ID

        Returns:
            Neighborhood dictionary
        """
        return self._request("GET", f"neighborhoods/{neighborhood_id}")

    # Village Methods
    def get_villages(
        self,
        district_id: Optional[int] = None,
        name: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
        sort: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of villages with optional filtering.

        Args:
            district_id: Filter by district ID
            name: Filter by village name (partial match)
            offset: Pagination offset
            limit: Maximum results to return
            sort: Sort field (prefix with - for descending)
            fields: Comma-separated list of fields to return

        Returns:
            List of village dictionaries
        """
        params = {
            "districtId": district_id,
            "name": name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "fields": fields,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "villages", params=params)

    def get_village(self, village_id: int) -> Dict[str, Any]:
        """
        Get specific village by ID.

        Args:
            village_id: Village ID

        Returns:
            Village dictionary
        """
        return self._request("GET", f"villages/{village_id}")

    # Town Methods
    def get_towns(
        self,
        district_id: Optional[int] = None,
        name: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
        sort: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of towns with optional filtering.

        Args:
            district_id: Filter by district ID
            name: Filter by town name (partial match)
            offset: Pagination offset
            limit: Maximum results to return
            sort: Sort field (prefix with - for descending)
            fields: Comma-separated list of fields to return

        Returns:
            List of town dictionaries
        """
        params = {
            "districtId": district_id,
            "name": name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "fields": fields,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "towns", params=params)

    def get_town(self, town_id: int) -> Dict[str, Any]:
        """
        Get specific town by ID.

        Args:
            town_id: Town ID

        Returns:
            Town dictionary
        """
        return self._request("GET", f"towns/{town_id}")

    # Utility Methods
    def health(self) -> Dict[str, Any]:
        """
        Check API health status.

        Returns:
            Health check response
        """
        url = f"{self.base_url}/health"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def set_language(self, language: str):
        """
        Set preferred language for responses.

        Args:
            language: Language code (en or tr)
        """
        if language not in ["en", "tr"]:
            raise ValueError("Language must be 'en' or 'tr'")
        self.language = language
