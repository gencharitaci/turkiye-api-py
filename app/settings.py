"""
Application settings using Pydantic Settings for type-safe configuration.

This module provides centralized configuration management with environment variable
support, validation, and sensible defaults.
"""

import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be overridden via environment variables.
    Example: ENVIRONMENT=production, ALLOWED_ORIGINS=http://example.com,http://api.example.com
    """

    # ============================================================================
    # Application Settings
    # ============================================================================
    app_name: str = "Turkiye API"
    app_version: str = "1.1.0"
    environment: str = "development"
    debug: bool = False

    # ============================================================================
    # Server Settings
    # ============================================================================
    host: str = "0.0.0.0"
    port: int = 8181
    workers: int = 0  # 0 means auto-calculate based on CPU count

    # ============================================================================
    # CORS Settings
    # ============================================================================
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:8181"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["GET", "POST", "OPTIONS"]
    cors_allow_headers: List[str] = ["Accept", "Accept-Language", "Content-Type", "X-Language"]
    cors_max_age: int = 600  # 10 minutes

    # ============================================================================
    # Cookie Settings
    # ============================================================================
    language_cookie_name: str = "language"
    language_cookie_max_age: int = 31_536_000  # 1 year
    language_cookie_path: str = "/"

    # ============================================================================
    # Logging Settings
    # ============================================================================
    log_level: str = "INFO"
    log_format: str = "json"  # "json" or "text"

    # ============================================================================
    # Rate Limiting Settings
    # ============================================================================
    rate_limit_enabled: bool = False
    rate_limit_per_minute: int = 60
    rate_limit_storage: str = "memory"  # "memory" or "redis"
    redis_url: str = "redis://localhost:6379"

    # ============================================================================
    # Metrics & Monitoring Settings
    # ============================================================================
    metrics_enabled: bool = True
    prometheus_enabled: bool = False

    # ============================================================================
    # Data Settings
    # ============================================================================
    data_dir: str = "app/data"

    # ============================================================================
    # Security Settings
    # ============================================================================
    expose_server_header: bool = False  # Set to True to add X-Powered-By header
    health_check_detailed: bool = True  # Set to False in production for minimal info
    health_check_auth_enabled: bool = False  # Enable authentication for /health endpoint
    health_check_username: str = "admin"
    health_check_password: str = ""  # Set via environment variable for security

    # Model configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    # ============================================================================
    # Computed Properties
    # ============================================================================

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @property
    def cookie_secure(self) -> bool:
        """Determine if cookies should be secure based on environment."""
        return self.is_production

    @property
    def cookie_samesite(self) -> str:
        """Determine cookie SameSite policy based on environment."""
        return "strict" if self.is_production else "lax"

    @property
    def effective_log_level(self) -> str:
        """Get effective log level based on environment and debug flag."""
        if self.debug:
            return "DEBUG"
        return self.log_level.upper()

    def get_allowed_origins_list(self) -> List[str]:
        """
        Get list of allowed origins from environment variable or default.

        Environment variable format: comma-separated list
        Example: ALLOWED_ORIGINS=http://example.com,http://api.example.com
        """
        env_origins = os.getenv("ALLOWED_ORIGINS")
        if env_origins:
            return [origin.strip() for origin in env_origins.split(",")]
        return self.allowed_origins


# Global settings instance
settings = Settings()
