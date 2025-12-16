"""
Unit tests for BaseService.

Tests the shared utility methods used across all service classes
including field filtering, sorting, and pagination validation.
"""

import pytest
from fastapi import HTTPException

from app.services.base_service import BaseService


class TestBaseService:
    """Test suite for BaseService utility methods."""

    @pytest.fixture
    def service(self):
        """Create BaseService instance for testing."""
        return BaseService()

    @pytest.fixture
    def sample_data(self):
        """Sample data for testing filtering and sorting."""
        return [
            {"id": 1, "name": "Adana", "population": 2000000, "area": 13844},
            {"id": 2, "name": "Istanbul", "population": 15000000, "area": 5461},
            {"id": 3, "name": "Ankara", "population": 5500000, "area": 25706},
        ]

    # Field Filtering Tests
    def test_filter_fields_returns_specified_fields_only(self, service):
        """Should return only specified fields from item."""
        item = {"id": 1, "name": "Test", "population": 1000, "extra": "data"}
        filtered = service._filter_fields(item, "id,name")
        assert set(filtered.keys()) == {"id", "name"}
        assert filtered["id"] == 1
        assert filtered["name"] == "Test"

    def test_filter_fields_returns_all_when_no_fields_specified(self, service):
        """Should return all fields when fields parameter is None."""
        item = {"id": 1, "name": "Test", "population": 1000}
        filtered = service._filter_fields(item, None)
        assert filtered == item

    def test_filter_fields_handles_whitespace(self, service):
        """Should handle whitespace in fields list."""
        item = {"id": 1, "name": "Test", "population": 1000}
        filtered = service._filter_fields(item, "id, name, population")
        assert set(filtered.keys()) == {"id", "name", "population"}

    # Sorting Tests
    def test_sort_data_ascending(self, service, sample_data):
        """Should sort data in ascending order."""
        sorted_data = service._sort_data(sample_data, "population")
        populations = [d["population"] for d in sorted_data]
        assert populations == sorted(populations)

    def test_sort_data_descending(self, service, sample_data):
        """Should sort data in descending order with '-' prefix."""
        sorted_data = service._sort_data(sample_data, "-population")
        populations = [d["population"] for d in sorted_data]
        assert populations == sorted(populations, reverse=True)

    def test_sort_data_by_string_field(self, service, sample_data):
        """Should sort data by string field (alphabetically)."""
        sorted_data = service._sort_data(sample_data, "name")
        names = [d["name"] for d in sorted_data]
        assert names == sorted(names)

    def test_sort_data_returns_unsorted_when_sort_is_none(self, service, sample_data):
        """Should return data as-is when sort parameter is None."""
        sorted_data = service._sort_data(sample_data, None)
        assert sorted_data == sample_data

    def test_sort_data_raises_on_invalid_field(self, service, sample_data):
        """Should raise HTTPException for invalid sort field."""
        with pytest.raises(HTTPException) as exc_info:
            service._sort_data(sample_data, "invalid_field")
        assert exc_info.value.status_code == 400
        assert "invalid sort field" in exc_info.value.detail.lower()

    # Pagination Validation Tests
    def test_validate_pagination_accepts_valid_values(self, service):
        """Should accept valid pagination parameters."""
        offset, limit = service.validate_pagination(10, 20, max_limit=100)
        assert offset == 10
        assert limit == 20

    def test_validate_pagination_clamps_limit_to_max(self, service):
        """Should clamp limit to max_limit with warning."""
        offset, limit = service.validate_pagination(0, 200, max_limit=100)
        assert limit == 100

    def test_validate_pagination_raises_on_negative_offset(self, service):
        """Should raise HTTPException for negative offset."""
        with pytest.raises(HTTPException) as exc_info:
            service.validate_pagination(-1, 10, max_limit=100)
        assert exc_info.value.status_code == 400
        assert "offset" in exc_info.value.detail.lower()

    def test_validate_pagination_raises_on_offset_exceeds_max(self, service):
        """Should raise HTTPException for offset > max_offset."""
        with pytest.raises(HTTPException) as exc_info:
            service.validate_pagination(200000, 10, max_limit=100)
        assert exc_info.value.status_code == 400
        assert "offset" in exc_info.value.detail.lower()

    def test_validate_pagination_raises_on_zero_limit(self, service):
        """Should raise HTTPException for limit = 0."""
        with pytest.raises(HTTPException) as exc_info:
            service.validate_pagination(0, 0, max_limit=100)
        assert exc_info.value.status_code == 400
        assert "limit" in exc_info.value.detail.lower()

    def test_validate_pagination_raises_on_negative_limit(self, service):
        """Should raise HTTPException for negative limit."""
        with pytest.raises(HTTPException) as exc_info:
            service.validate_pagination(0, -5, max_limit=100)
        assert exc_info.value.status_code == 400
        assert "limit" in exc_info.value.detail.lower()

    def test_validate_pagination_accepts_zero_offset(self, service):
        """Should accept offset = 0 (start of list)."""
        offset, limit = service.validate_pagination(0, 10, max_limit=100)
        assert offset == 0
        assert limit == 10
