"""
Application configuration constants.

This module centralizes all configuration values, limits, and constants
used throughout the application to avoid magic numbers and improve maintainability.
"""

# ============================================================================
# PAGINATION LIMITS
# ============================================================================

# Maximum number of results per resource type
MAX_LIMIT_PROVINCES = 81  # Only 81 provinces in Turkey
MAX_LIMIT_DISTRICTS = 1000
MAX_LIMIT_NEIGHBORHOODS = 50000  # Approximately 50,000 neighborhoods
MAX_LIMIT_VILLAGES = 50000  # Approximately 50,000 villages
MAX_LIMIT_TOWNS = 10000

# Default limits when not specified
DEFAULT_LIMIT_PROVINCES = 81
DEFAULT_LIMIT_DISTRICTS = 100
DEFAULT_LIMIT_NEIGHBORHOODS = 100
DEFAULT_LIMIT_VILLAGES = 100
DEFAULT_LIMIT_TOWNS = 100

# Maximum offset for pagination (prevents excessive memory usage)
MAX_OFFSET = 100000


# ============================================================================
# DATA VALIDATION BOUNDS
# ============================================================================

# Population bounds
DEFAULT_MIN_POPULATION = 1
DEFAULT_MAX_POPULATION = 1_000_000_000  # 1 billion (theoretical maximum)

# Area bounds (in square kilometers)
DEFAULT_MIN_AREA = 1
DEFAULT_MAX_AREA = 1_000_000_000  # 1 billion km² (theoretical maximum)

# Altitude bounds (in meters)
DEFAULT_MIN_ALTITUDE = 0  # Sea level
DEFAULT_MAX_ALTITUDE = 10_000  # 10,000 meters (theoretical maximum for Turkey)


# ============================================================================
# COOKIE & SESSION CONFIGURATION
# ============================================================================

# Language cookie settings
LANGUAGE_COOKIE_NAME = "language"
LANGUAGE_COOKIE_MAX_AGE = 31_536_000  # 1 year in seconds (365 * 24 * 60 * 60)
LANGUAGE_COOKIE_PATH = "/"

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

# CORS preflight cache duration
PREFLIGHT_CACHE_MAX_AGE = 600  # 10 minutes in seconds


# ============================================================================
# WORKER & SERVER CONFIGURATION
# ============================================================================

# Gunicorn worker multiplier (workers = cpu_count * WORKERS_MULTIPLIER + 1)
DEFAULT_WORKERS_MULTIPLIER = 2


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Default log levels
DEFAULT_LOG_LEVEL = "INFO"
DEVELOPMENT_LOG_LEVEL = "DEBUG"
PRODUCTION_LOG_LEVEL = "WARNING"


# ============================================================================
# API METADATA
# ============================================================================

# Expected data counts for health checks
EXPECTED_PROVINCE_COUNT = 81
