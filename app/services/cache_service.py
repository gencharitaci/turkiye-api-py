"""
Enhanced caching service for query results.

This module provides Redis-based caching for frequently accessed data
to improve performance and reduce data processing overhead.
"""

import hashlib
import json
import logging
from typing import Any, Optional

from app.settings import settings

logger = logging.getLogger(__name__)


class CacheService:
    """
    Cache service with Redis backend support.

    Provides caching functionality for API responses with automatic
    key generation, TTL management, and cache invalidation.
    """

    def __init__(self):
        """Initialize cache service with Redis connection if enabled."""
        self.enabled = False
        self.redis_client = None

        # Only initialize Redis if URL is configured and not using default localhost
        if settings.redis_url and settings.redis_url != "redis://localhost:6379":
            try:
                import redis

                self.redis_client = redis.from_url(
                    settings.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,  # Increased from 2s to 5s for better reliability
                    socket_timeout=5,
                    retry_on_timeout=True,  # Added retry on timeout
                    health_check_interval=30,  # Added health check
                )
                # Test connection with retry
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        self.redis_client.ping()
                        self.enabled = True
                        logger.info(f"Cache service initialized with Redis: {settings.redis_url}")
                        break
                    except Exception as retry_error:
                        if attempt < max_retries - 1:
                            logger.warning(f"Redis connection attempt {attempt + 1} failed, retrying...")
                            continue
                        raise retry_error
            except ImportError:
                logger.warning("Redis library not installed, caching disabled. Install with: pip install redis")
                self.enabled = False
            except Exception as e:
                logger.warning(f"Redis cache not available, falling back to no caching: {e}")
                self.enabled = False
        else:
            logger.info("Cache service disabled (Redis not configured)")

    def generate_key(self, prefix: str, **kwargs) -> str:
        """
        Generate cache key from prefix and parameters.

        Args:
            prefix: Key prefix (e.g., "provinces", "districts")
            **kwargs: Parameters to include in key generation

        Returns:
            Generated cache key string
        """
        # Sort kwargs for consistent key generation
        sorted_params = sorted(kwargs.items())
        params_str = json.dumps(sorted_params, sort_keys=True)

        # Hash parameters for shorter keys
        params_hash = hashlib.md5(params_str.encode()).hexdigest()[:12]

        return f"turkiye_api:{prefix}:{params_hash}"

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value by key.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/error
        """
        if not self.enabled or not self.redis_client:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 1800) -> bool:
        """
        Cache value with TTL.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (default: 1800 = 30 minutes)

        Returns:
            True if cached successfully, False otherwise
        """
        if not self.enabled or not self.redis_client:
            return False

        try:
            serialized = json.dumps(value)
            self.redis_client.setex(key, ttl, serialized)
            logger.debug(f"Cached: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> None:
        """
        Delete cached value.

        Args:
            key: Cache key to delete
        """
        if not self.enabled or not self.redis_client:
            return

        try:
            self.redis_client.delete(key)
            logger.debug(f"Cache deleted: {key}")
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")

    def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalidate all keys matching pattern.

        Args:
            pattern: Pattern to match (e.g., "turkiye_api:provinces:*")
        """
        if not self.enabled or not self.redis_client:
            return

        try:
            keys = list(self.redis_client.scan_iter(match=pattern))
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} keys matching pattern: {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidate error for pattern {pattern}: {e}")

    def clear(self) -> None:
        """Clear all cache entries for this application."""
        if not self.enabled or not self.redis_client:
            return

        try:
            self.invalidate_pattern("turkiye_api:*")
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


# Global cache service instance
cache_service = CacheService()
