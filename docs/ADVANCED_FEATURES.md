# Advanced Features Guide

This guide covers the advanced features available in Turkiye API including rate limiting, Redis caching, API versioning, and monitoring.

## Table of Contents

- [Rate Limiting](#rate-limiting)
- [Redis Integration](#redis-integration)
- [API Versioning](#api-versioning)
- [Monitoring & Metrics](#monitoring--metrics)
- [Configuration](#configuration)

---

## Rate Limiting

The API includes built-in rate limiting to prevent abuse and ensure fair usage across all clients.

### Features

- **Flexible Storage**: Supports both in-memory and Redis-based storage
- **Smart Client Detection**: Identifies clients via IP, X-Forwarded-For, or X-Real-IP headers
- **Rate Limit Headers**: Responses include rate limit information in headers
- **Fixed-Window Strategy**: Uses fixed-window rate limiting algorithm

### Configuration

Set the following environment variables:

```bash
# Enable/disable rate limiting
RATE_LIMIT_ENABLED=true

# Requests per minute per client
RATE_LIMIT_PER_MINUTE=60

# Storage backend: "memory" or "redis"
RATE_LIMIT_STORAGE=memory

# Redis URL (only if using Redis storage)
REDIS_URL=redis://localhost:6379
```

### Using Rate Limiting

When rate limiting is enabled, API responses include the following headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640000000
```

If you exceed the rate limit, you'll receive a `429 Too Many Requests` response:

```json
{
  "error": "Rate limit exceeded: 60 per 1 minute"
}
```

### Example: Enable Rate Limiting with Redis

```bash
# .env file
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_STORAGE=redis
REDIS_URL=redis://localhost:6379
```

---

## Redis Integration

Redis can be used for distributed rate limiting, which is essential for multi-instance deployments.

### Why Use Redis?

- **Distributed Rate Limiting**: Share rate limit state across multiple API instances
- **Scalability**: Handle high-traffic scenarios with consistent rate limiting
- **Persistence**: Rate limit data survives application restarts
- **Performance**: Fast in-memory operations

### Setup Redis

#### Local Development (Docker)

```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

#### Production

For production, use a managed Redis service:
- **AWS**: Amazon ElastiCache for Redis
- **Google Cloud**: Cloud Memorystore for Redis
- **Azure**: Azure Cache for Redis
- **Self-hosted**: Redis Cluster

### Configuration

```bash
# .env file
REDIS_URL=redis://username:password@hostname:6379/0

# Or for Redis Sentinel
REDIS_URL=redis+sentinel://sentinel-host:26379/mymaster/0

# Or for Redis Cluster
REDIS_URL=redis://host1:7000,host2:7001,host3:7002/0
```

### Connection String Format

```
redis://[:password@]host[:port][/database]
```

Examples:
- Local: `redis://localhost:6379`
- With auth: `redis://:mypassword@redis.example.com:6379`
- Specific DB: `redis://localhost:6379/1`
- With username: `redis://myuser:mypassword@localhost:6379`

---

## API Versioning

The API supports versioning to enable smooth migrations and backward compatibility.

### Current Version

- **Default Version**: v1
- **Latest Version**: v1
- **Supported Versions**: v1

### Versioning Strategies

The API supports multiple ways to specify the version:

#### 1. URL Path (Recommended)

```bash
GET https://api.example.com/api/v1/provinces
GET https://api.example.com/api/v2/provinces  # Future version
```

#### 2. Header-Based

```bash
curl -H "X-API-Version: v1" https://api.example.com/api/provinces
```

#### 3. Default Version

If no version is specified, the default version (v1) is used.

### Version Information Endpoint

Get information about all supported API versions:

```bash
GET /api/versions
```

Response:

```json
{
  "current_version": "v1",
  "default_version": "v1",
  "supported_versions": [
    {
      "version": "v1",
      "status": "current",
      "deprecated": false
    }
  ]
}
```

### Version Headers

All API responses include version information in headers:

```
X-API-Version: v1
X-API-Latest-Version: v1
```

### Deprecation Process

When a version is deprecated, the API will include additional headers:

```
X-API-Deprecated: true
X-API-Sunset-Date: 2026-12-31
X-API-Alternative-Version: v2
```

### Future Versions

The versioning infrastructure is ready to support v2 and beyond. When v2 is released:

1. New endpoints will be available at `/api/v2/...`
2. v1 endpoints will continue to work
3. Deprecation timeline will be announced
4. Migration guides will be provided

### Best Practices

1. **Always specify version**: Use `/api/v1/...` instead of relying on defaults
2. **Monitor deprecation headers**: Watch for `X-API-Deprecated` in responses
3. **Test new versions early**: Try beta versions before they become default
4. **Subscribe to changes**: Follow the repository for version announcements

---

## Monitoring & Metrics

The API includes comprehensive monitoring and metrics collection.

### Prometheus Metrics

When enabled, the API exposes Prometheus-compatible metrics at `/metrics`.

#### Configuration

```bash
# .env file
PROMETHEUS_ENABLED=true
```

#### Available Metrics

**HTTP Metrics:**
- `http_requests_total` - Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_in_progress` - Current in-flight requests

**Application Metrics:**
- `app_info` - Application version and environment information
- `data_loader_provinces_total` - Total number of provinces loaded
- `data_loader_districts_total` - Total number of districts loaded
- `data_loader_neighborhoods_total` - Total number of neighborhoods loaded
- `data_loader_villages_total` - Total number of villages loaded
- `data_loader_towns_total` - Total number of towns loaded

**Request Metrics (Custom Middleware):**
- Request counts by endpoint
- Response times
- Error rates

#### Accessing Metrics

```bash
curl http://localhost:8181/metrics
```

### Health Checks

Enhanced health check endpoint with dependency validation:

```bash
GET /health
```

Response:

```json
{
  "status": "ok",
  "uptime_seconds": 3600,
  "timestamp": "2025-12-14T10:30:00Z",
  "environment": "production",
  "version": "1.0.0",
  "checks": {
    "data_loader": {
      "status": "ok",
      "provinces": 81,
      "districts": 973
    }
  }
}
```

### Logging

Structured JSON logging for production environments:

```bash
# .env file
LOG_LEVEL=INFO
LOG_FORMAT=json  # or "text" for development
ENVIRONMENT=production
```

Log output includes:
- Timestamp
- Log level
- Message
- Request ID (if applicable)
- User context
- Additional metadata

---

## Configuration

### Complete Environment Variables Reference

```bash
# ============================================================================
# Application Settings
# ============================================================================
APP_NAME=Turkiye API
APP_VERSION=1.0.0
ENVIRONMENT=production  # or "development", "staging"
DEBUG=false

# ============================================================================
# Server Settings
# ============================================================================
HOST=0.0.0.0
PORT=8181
WORKERS=0  # 0 = auto-calculate based on CPU count

# ============================================================================
# CORS Settings
# ============================================================================
ALLOWED_ORIGINS=http://localhost:3000,https://example.com
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,OPTIONS
CORS_ALLOW_HEADERS=Accept,Accept-Language,Content-Type,X-Language,X-API-Version

# ============================================================================
# Cookie Settings
# ============================================================================
LANGUAGE_COOKIE_NAME=language
LANGUAGE_COOKIE_MAX_AGE=31536000  # 1 year
LANGUAGE_COOKIE_PATH=/

# ============================================================================
# Logging Settings
# ============================================================================
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # "json" or "text"

# ============================================================================
# Rate Limiting Settings
# ============================================================================
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_STORAGE=redis  # "memory" or "redis"
REDIS_URL=redis://localhost:6379

# ============================================================================
# Metrics & Monitoring Settings
# ============================================================================
METRICS_ENABLED=true
PROMETHEUS_ENABLED=true

# ============================================================================
# Data Settings
# ============================================================================
DATA_DIR=app/data
```

### Configuration Validation

The application uses Pydantic Settings for type-safe configuration with automatic validation:

```python
from app.settings import settings

# All settings are validated and type-safe
print(settings.rate_limit_per_minute)  # int
print(settings.is_production)  # bool
print(settings.get_allowed_origins_list())  # List[str]
```

### Production Checklist

Before deploying to production, ensure:

- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`
- [ ] `ALLOWED_ORIGINS` is set to specific domains (not `*`)
- [ ] `RATE_LIMIT_ENABLED=true`
- [ ] `RATE_LIMIT_STORAGE=redis` (for multi-instance deployments)
- [ ] `PROMETHEUS_ENABLED=true` (for monitoring)
- [ ] `LOG_FORMAT=json` (for log aggregation)
- [ ] `LOG_LEVEL=INFO` or `WARNING`
- [ ] Redis is properly configured and accessible
- [ ] SSL/TLS is enabled (cookies will be secure automatically)

---

## Examples

### Example 1: Development Setup (In-Memory)

```bash
# .env
ENVIRONMENT=development
DEBUG=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_STORAGE=memory
PROMETHEUS_ENABLED=false
LOG_FORMAT=text
```

### Example 2: Production Setup (Redis)

```bash
# .env
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://myapp.com,https://api.myapp.com
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_STORAGE=redis
REDIS_URL=redis://:mypassword@redis.production.example.com:6379/0
PROMETHEUS_ENABLED=true
LOG_FORMAT=json
LOG_LEVEL=INFO
```

### Example 3: High-Traffic Setup

```bash
# .env
ENVIRONMENT=production
WORKERS=4  # Or 0 for auto
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=200
RATE_LIMIT_STORAGE=redis
REDIS_URL=redis://redis-cluster.example.com:6379/0
PROMETHEUS_ENABLED=true
METRICS_ENABLED=true
```

---

## Troubleshooting

### Rate Limiting Issues

**Problem**: Rate limits not shared across instances

**Solution**: Switch from `memory` to `redis` storage:
```bash
RATE_LIMIT_STORAGE=redis
REDIS_URL=redis://your-redis-host:6379
```

**Problem**: Redis connection errors

**Solution**: Check Redis connectivity:
```bash
redis-cli -h your-redis-host -p 6379 ping
```

### Versioning Issues

**Problem**: Getting "Unsupported API version" error

**Solution**: Use a supported version path:
```bash
# Instead of:
GET /api/v3/provinces  # ❌

# Use:
GET /api/v1/provinces  # ✅
```

### Monitoring Issues

**Problem**: Metrics endpoint returns 404

**Solution**: Enable Prometheus metrics:
```bash
PROMETHEUS_ENABLED=true
```

---

## Next Steps

- [Deployment Guide](DEPLOYMENT_EN.md) - Deploy to production
- [Multi-Language Documentation](MULTI_LANGUAGE_DOCS.md) - i18n features
- [API Reference](http://localhost:8181/docs) - Interactive API documentation

---

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/gencharitaci/turkiye-api-py/issues
- Email: gncharitaci@gmail.com
