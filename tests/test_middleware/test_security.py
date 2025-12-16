"""
Unit tests for SecurityHeadersMiddleware.

Tests the OWASP-compliant security headers added to all responses.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.security import SecurityHeadersMiddleware


class TestSecurityHeadersMiddleware:
    """Test suite for SecurityHeadersMiddleware."""

    @pytest.fixture
    def app(self):
        """Create minimal FastAPI app with security middleware."""
        app = FastAPI()

        # Add security middleware
        app.add_middleware(SecurityHeadersMiddleware, expose_server_header=False)

        @app.get("/test")
        def test_endpoint():
            return {"message": "test"}

        return app

    @pytest.fixture
    def app_with_server_header(self):
        """Create app with server header exposed."""
        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware, expose_server_header=True)

        @app.get("/test")
        def test_endpoint():
            return {"message": "test"}

        return app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def client_with_server_header(self, app_with_server_header):
        """Create test client with server header."""
        return TestClient(app_with_server_header)

    def test_x_content_type_options_header_added(self, client):
        """Should add X-Content-Type-Options: nosniff header."""
        response = client.get("/test")
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"

    def test_x_frame_options_header_added(self, client):
        """Should add X-Frame-Options: DENY header."""
        response = client.get("/test")
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"

    def test_x_xss_protection_header_added(self, client):
        """Should add X-XSS-Protection header."""
        response = client.get("/test")
        assert "x-xss-protection" in response.headers
        assert response.headers["x-xss-protection"] == "1; mode=block"

    def test_content_security_policy_header_added(self, client):
        """Should add Content-Security-Policy header."""
        response = client.get("/test")
        assert "content-security-policy" in response.headers
        csp = response.headers["content-security-policy"]
        assert "default-src 'self'" in csp
        assert "script-src" in csp
        assert "style-src" in csp

    def test_referrer_policy_header_added(self, client):
        """Should add Referrer-Policy header."""
        response = client.get("/test")
        assert "referrer-policy" in response.headers
        assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"

    def test_permissions_policy_header_added(self, client):
        """Should add Permissions-Policy header."""
        response = client.get("/test")
        assert "permissions-policy" in response.headers
        policy = response.headers["permissions-policy"]
        assert "geolocation=()" in policy
        assert "microphone=()" in policy
        assert "camera=()" in policy

    def test_x_powered_by_not_added_by_default(self, client):
        """Should NOT add X-Powered-By header by default (security)."""
        response = client.get("/test")
        assert "x-powered-by" not in response.headers

    def test_x_powered_by_added_when_enabled(self, client_with_server_header):
        """Should add X-Powered-By header when explicitly enabled."""
        response = client_with_server_header.get("/test")
        assert "x-powered-by" in response.headers
        assert response.headers["x-powered-by"] == "Turkiye-API"

    def test_all_security_headers_present(self, client):
        """Should add all required security headers."""
        response = client.get("/test")

        required_headers = [
            "x-content-type-options",
            "x-frame-options",
            "x-xss-protection",
            "content-security-policy",
            "referrer-policy",
            "permissions-policy",
        ]

        for header in required_headers:
            assert header in response.headers, f"Missing security header: {header}"

    def test_security_headers_on_error_responses(self, client):
        """Should add security headers even on error responses."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
