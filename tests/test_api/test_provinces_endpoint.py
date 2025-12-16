"""
Integration tests for provinces API endpoints.

Tests the full HTTP request/response cycle for province endpoints
including status codes, response format, and error handling.
"""


class TestProvincesEndpoint:
    """Test suite for /api/v1/provinces endpoints."""

    def test_get_provinces_returns_200(self, client):
        """GET /api/v1/provinces should return 200 with all provinces."""
        response = client.get("/api/v1/provinces")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "OK"
        assert "data" in data
        assert len(data["data"]) == 81

    def test_get_provinces_with_name_filter(self, client):
        """Should filter provinces by name query parameter."""
        response = client.get("/api/v1/provinces?name=Adana")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "OK"
        assert len(data["data"]) >= 1
        assert all("Adana" in p["name"] for p in data["data"])

    def test_get_provinces_with_population_filter(self, client):
        """Should filter provinces by population range."""
        response = client.get("/api/v1/provinces?minPopulation=1000000&maxPopulation=5000000")
        assert response.status_code == 200

        data = response.json()
        provinces = data["data"]
        assert all(1000000 <= p["population"] <= 5000000 for p in provinces)

    def test_get_provinces_with_coastal_filter(self, client):
        """Should filter provinces by coastal status."""
        response = client.get("/api/v1/provinces?isCoastal=true")
        assert response.status_code == 200

        data = response.json()
        assert all(p["isCoastal"] is True for p in data["data"])

    def test_get_provinces_with_pagination(self, client):
        """Should support offset and limit pagination."""
        response = client.get("/api/v1/provinces?offset=10&limit=5")
        assert response.status_code == 200

        data = response.json()
        assert len(data["data"]) == 5

    def test_get_provinces_with_sorting(self, client):
        """Should sort provinces by specified field."""
        response = client.get("/api/v1/provinces?sort=population&limit=10")
        assert response.status_code == 200

        data = response.json()
        populations = [p["population"] for p in data["data"]]
        assert populations == sorted(populations)

    def test_get_provinces_with_descending_sort(self, client):
        """Should sort provinces in descending order with '-' prefix."""
        response = client.get("/api/v1/provinces?sort=-population&limit=10")
        assert response.status_code == 200

        data = response.json()
        populations = [p["population"] for p in data["data"]]
        assert populations == sorted(populations, reverse=True)

    def test_get_provinces_with_field_selection(self, client):
        """Should return only requested fields."""
        response = client.get("/api/v1/provinces?fields=id,name,population&limit=1")
        assert response.status_code == 200

        data = response.json()
        province = data["data"][0]
        assert set(province.keys()) == {"id", "name", "population"}

    def test_get_provinces_returns_404_for_invalid_range(self, client):
        """Should return 404 for invalid population range."""
        response = client.get("/api/v1/provinces?minPopulation=2000000&maxPopulation=500000")
        assert response.status_code == 404

        data = response.json()
        assert data["status"] == "ERROR"
        assert "minimum population cannot be greater" in data["error"].lower()

    def test_get_provinces_returns_400_for_invalid_sort(self, client):
        """Should return 400 for invalid sort field."""
        response = client.get("/api/v1/provinces?sort=invalid_field")
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data

    def test_get_province_by_id_returns_200(self, client):
        """GET /api/v1/provinces/{id} should return specific province."""
        response = client.get("/api/v1/provinces/1")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "OK"
        province = data["data"]
        assert province["id"] == 1
        assert province["name"] == "Adana"
        assert "districts" in province

    def test_get_province_by_id_returns_404_for_invalid_id(self, client):
        """Should return 404 for non-existent province ID."""
        response = client.get("/api/v1/provinces/999")
        assert response.status_code == 404

        data = response.json()
        assert data["status"] == "ERROR"
        assert "not found" in data["error"].lower()

    def test_get_province_with_extend(self, client):
        """Should include neighborhoods and villages when extend=true."""
        response = client.get("/api/v1/provinces/1?extend=true")
        assert response.status_code == 200

        data = response.json()
        province = data["data"]
        assert "districts" in province

        # Check first district has nested data
        if len(province["districts"]) > 0:
            district = province["districts"][0]
            assert "neighborhoods" in district
            assert "villages" in district

    def test_get_province_with_field_selection(self, client):
        """Should return only requested fields for specific province."""
        response = client.get("/api/v1/provinces/1?fields=id,name,population")
        assert response.status_code == 200

        data = response.json()
        province = data["data"]
        assert set(province.keys()) == {"id", "name", "population"}

    def test_health_endpoint_returns_ok(self, client):
        """GET /health should return ok status."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"
        assert "uptime" in data
        assert "timestamp" in data

    def test_root_endpoint_returns_ok(self, client):
        """GET / should return welcome message."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "OK"
        assert "message" in data
