"""
Unit tests for DataLoader.

Tests the singleton pattern, data loading, caching,
and pre-indexed lookup functionality.
"""

from app.services.data_loader import DataLoader, data_loader


class TestDataLoader:
    """Test suite for DataLoader class."""

    def test_singleton_pattern(self):
        """DataLoader should implement singleton pattern."""
        loader1 = DataLoader()
        loader2 = DataLoader()
        assert loader1 is loader2
        assert id(loader1) == id(loader2)

    def test_module_level_instance_is_singleton(self):
        """Module-level data_loader should be the singleton instance."""
        loader = DataLoader()
        assert loader is data_loader

    def test_provinces_loaded(self, data_loader):
        """Should load exactly 81 provinces from Turkey."""
        provinces = data_loader.provinces
        assert len(provinces) == 81
        assert all(isinstance(p, dict) for p in provinces)

    def test_districts_loaded(self, data_loader):
        """Should load districts data."""
        districts = data_loader.districts
        assert len(districts) > 0
        assert all(isinstance(d, dict) for d in districts)
        assert all("provinceId" in d for d in districts)

    def test_neighborhoods_loaded(self, data_loader):
        """Should load neighborhoods data."""
        neighborhoods = data_loader.neighborhoods
        assert len(neighborhoods) > 0
        assert all(isinstance(n, dict) for n in neighborhoods)
        assert all("districtId" in n for n in neighborhoods)

    def test_villages_loaded(self, data_loader):
        """Should load villages data."""
        villages = data_loader.villages
        assert len(villages) > 0
        assert all(isinstance(v, dict) for v in villages)
        assert all("districtId" in v for v in villages)

    def test_towns_loaded(self, data_loader):
        """Should load towns data."""
        towns = data_loader.towns
        assert len(towns) > 0
        assert all(isinstance(t, dict) for t in towns)
        assert all("districtId" in t for t in towns)

    def test_data_cached(self, data_loader):
        """Should cache loaded data (same object reference)."""
        provinces1 = data_loader.provinces
        provinces2 = data_loader.provinces
        assert provinces1 is provinces2

    def test_districts_by_province_index(self, data_loader):
        """Should provide pre-indexed districts by province ID."""
        index = data_loader.districts_by_province
        assert isinstance(index, dict)
        assert len(index) > 0

        # Check index structure
        for province_id, districts in index.items():
            assert isinstance(province_id, int)
            assert isinstance(districts, list)
            assert all(isinstance(d, dict) for d in districts)
            assert all(d["id"] and d["name"] for d in districts)

    def test_neighborhoods_by_district_index(self, data_loader):
        """Should provide pre-indexed neighborhoods by district ID."""
        index = data_loader.neighborhoods_by_district
        assert isinstance(index, dict)
        assert len(index) > 0

        # Check index structure
        for district_id, neighborhoods in index.items():
            assert isinstance(district_id, int)
            assert isinstance(neighborhoods, list)
            assert all(isinstance(n, dict) for n in neighborhoods)

    def test_villages_by_district_index(self, data_loader):
        """Should provide pre-indexed villages by district ID."""
        index = data_loader.villages_by_district
        assert isinstance(index, dict)
        assert len(index) > 0

        # Check index structure
        for district_id, villages in index.items():
            assert isinstance(district_id, int)
            assert isinstance(villages, list)
            assert all(isinstance(v, dict) for v in villages)

    def test_index_caching(self, data_loader):
        """Should cache indexed data (same object reference)."""
        index1 = data_loader.districts_by_province
        index2 = data_loader.districts_by_province
        assert index1 is index2

    def test_province_data_structure(self, data_loader):
        """Provinces should have expected structure."""
        province = data_loader.provinces[0]
        required_fields = ["id", "name", "population", "area", "isCoastal", "isMetropolitan"]
        for field in required_fields:
            assert field in province

    def test_district_data_structure(self, data_loader):
        """Districts should have expected structure."""
        district = data_loader.districts[0]
        required_fields = ["id", "provinceId", "name", "population", "area"]
        for field in required_fields:
            assert field in district
