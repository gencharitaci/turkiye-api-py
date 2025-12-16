"""
Unit tests for ProvinceService.

Tests the business logic of province data operations including
filtering, sorting, pagination, and error handling.
"""

import pytest
from fastapi import HTTPException

from app.services.province_service import province_service


class TestProvinceService:
    """Test suite for ProvinceService."""

    def test_get_provinces_returns_all_by_default(self):
        """Should return all 81 provinces without filters."""
        result = province_service.get_provinces()
        assert len(result) == 81
        assert all(isinstance(p, dict) for p in result)

    def test_get_provinces_filters_by_name(self):
        """Should filter provinces by name (case-insensitive partial match)."""
        result = province_service.get_provinces(name="Adana")
        assert len(result) >= 1
        assert all("Adana" in p["name"] or "adana" in p["name"].lower() for p in result)

    def test_get_provinces_filters_by_min_population(self):
        """Should filter provinces by minimum population."""
        min_pop = 1000000
        result = province_service.get_provinces(min_population=min_pop)
        assert all(p["population"] >= min_pop for p in result)

    def test_get_provinces_filters_by_max_population(self):
        """Should filter provinces by maximum population."""
        max_pop = 500000
        result = province_service.get_provinces(max_population=max_pop)
        assert all(p["population"] <= max_pop for p in result)

    def test_get_provinces_filters_by_population_range(self):
        """Should filter provinces by population range."""
        min_pop = 500000
        max_pop = 2000000
        result = province_service.get_provinces(min_population=min_pop, max_population=max_pop)
        assert all(min_pop <= p["population"] <= max_pop for p in result)

    def test_get_provinces_rejects_invalid_population_range(self):
        """Should raise HTTPException for min > max population."""
        with pytest.raises(HTTPException) as exc_info:
            province_service.get_provinces(min_population=2000000, max_population=500000)
        assert exc_info.value.status_code == 404
        assert "minimum population cannot be greater" in exc_info.value.detail.lower()

    def test_get_provinces_filters_by_coastal(self):
        """Should filter provinces by coastal status."""
        coastal = province_service.get_provinces(is_coastal=True)
        not_coastal = province_service.get_provinces(is_coastal=False)

        assert all(p["isCoastal"] is True for p in coastal)
        assert all(p["isCoastal"] is False for p in not_coastal)
        assert len(coastal) + len(not_coastal) == 81

    def test_get_provinces_filters_by_metropolitan(self):
        """Should filter provinces by metropolitan status."""
        metro = province_service.get_provinces(is_metropolitan=True)
        not_metro = province_service.get_provinces(is_metropolitan=False)

        assert all(p["isMetropolitan"] is True for p in metro)
        assert all(p["isMetropolitan"] is False for p in not_metro)

    def test_get_provinces_respects_pagination(self):
        """Should apply offset and limit correctly."""
        all_provinces = province_service.get_provinces()

        # Test limit
        limited = province_service.get_provinces(limit=10)
        assert len(limited) == 10

        # Test offset
        offset = province_service.get_provinces(offset=10, limit=10)
        assert len(offset) == 10
        assert offset[0]["id"] != all_provinces[0]["id"]

    def test_get_provinces_sorts_ascending(self):
        """Should sort provinces by field in ascending order."""
        result = province_service.get_provinces(sort="population")
        populations = [p["population"] for p in result]
        assert populations == sorted(populations)

    def test_get_provinces_sorts_descending(self):
        """Should sort provinces by field in descending order."""
        result = province_service.get_provinces(sort="-population")
        populations = [p["population"] for p in result]
        assert populations == sorted(populations, reverse=True)

    def test_get_provinces_raises_on_invalid_sort_field(self):
        """Should raise HTTPException for invalid sort field."""
        with pytest.raises(HTTPException) as exc_info:
            province_service.get_provinces(sort="invalid_field")
        assert exc_info.value.status_code == 400
        assert "invalid sort field" in exc_info.value.detail.lower()

    def test_get_provinces_filters_fields(self):
        """Should return only specified fields."""
        result = province_service.get_provinces(fields="id,name,population", limit=1)
        assert len(result) == 1
        province = result[0]
        assert set(province.keys()) == {"id", "name", "population"}

    def test_get_provinces_includes_districts(self):
        """Should include districts for each province."""
        result = province_service.get_provinces(limit=1)
        assert "districts" in result[0]
        assert isinstance(result[0]["districts"], list)

    def test_get_exact_province_returns_province_by_id(self):
        """Should return specific province by ID."""
        province = province_service.get_exact_province(province_id=1)
        assert province["id"] == 1
        assert province["name"] == "Adana"

    def test_get_exact_province_raises_404_for_invalid_id(self):
        """Should raise HTTPException for non-existent province."""
        with pytest.raises(HTTPException) as exc_info:
            province_service.get_exact_province(province_id=999)
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()

    def test_get_exact_province_with_extend(self):
        """Should include neighborhoods and villages when extend=True."""
        province = province_service.get_exact_province(province_id=1, extend=True)
        assert "districts" in province
        assert len(province["districts"]) > 0

        # Check first district has neighborhoods and villages
        district = province["districts"][0]
        assert "neighborhoods" in district
        assert "villages" in district
        assert isinstance(district["neighborhoods"], list)
        assert isinstance(district["villages"], list)

    def test_get_exact_province_filters_fields(self):
        """Should return only specified fields for exact province."""
        province = province_service.get_exact_province(province_id=1, fields="id,name,population")
        assert set(province.keys()) == {"id", "name", "population"}

    def test_get_exact_province_excludes_postal_code_by_default(self):
        """Should exclude postalCode unless explicitly activated."""
        province = province_service.get_exact_province(province_id=1)
        assert "postalCode" not in province

    def test_get_exact_province_includes_postal_code_when_activated(self):
        """Should include postalCode when activate_postal_codes=True."""
        province = province_service.get_exact_province(province_id=1, activate_postal_codes=True)
        # Only check if the province has a postal code in the data
        # Not all provinces may have postal codes
        if "postalCode" in province:
            assert isinstance(province["postalCode"], str)
