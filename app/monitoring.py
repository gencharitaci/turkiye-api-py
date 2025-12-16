"""
Prometheus metrics and monitoring instrumentation.

This module provides Prometheus metrics collection for observability,
enabling monitoring of API performance, usage, and health.
"""

import logging

from prometheus_client import Counter, Gauge, Histogram, Info
from prometheus_fastapi_instrumentator import Instrumentator, metrics

logger = logging.getLogger(__name__)


# Custom metrics
api_requests_total = Counter(
    "turkiye_api_requests_total", "Total number of API requests", ["method", "endpoint", "status_code"]
)

api_response_size_bytes = Histogram("turkiye_api_response_size_bytes", "API response size in bytes", ["endpoint"])

data_loader_items = Gauge("turkiye_api_data_items", "Number of items loaded in data loader", ["data_type"])

app_info = Info("turkiye_api_info", "Application information")


def setup_prometheus_metrics(app, enabled: bool = True):
    """
    Configure Prometheus metrics instrumentation for the FastAPI application.

    This sets up automatic instrumentation for:
    - Request count by method, endpoint, and status code
    - Request duration histograms
    - Request size histograms
    - Response size histograms
    - Active requests gauge
    - Custom business metrics

    Args:
        app: FastAPI application instance
        enabled: Whether to enable Prometheus metrics

    Returns:
        Instrumentator instance or None if disabled
    """
    if not enabled:
        logger.info("Prometheus metrics are disabled")
        return None

    # Create instrumentator with custom settings
    instrumentator = Instrumentator(
        should_group_status_codes=False,  # Track individual status codes
        should_ignore_untemplated=False,  # Track all endpoints
        should_respect_env_var=True,  # Respect ENABLE_METRICS env var
        should_instrument_requests_inprogress=True,  # Track active requests
        excluded_handlers=["/metrics", "/health", "/docs", "/redoc", "/openapi.json"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="turkiye_api_requests_inprogress",
        inprogress_labels=True,
    )

    # Add default metrics
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_name="turkiye_api_request_size_bytes",
            metric_doc="Request size in bytes",
        )
    )

    instrumentator.add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_name="turkiye_api_response_size_bytes",
            metric_doc="Response size in bytes",
        )
    )

    instrumentator.add(
        metrics.latency(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_name="turkiye_api_request_duration_seconds",
            metric_doc="Request duration in seconds",
        )
    )

    instrumentator.add(
        metrics.requests(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
            metric_name="turkiye_api_requests_total",
            metric_doc="Total number of requests",
        )
    )

    # Instrument the app
    instrumentator.instrument(app)

    # Expose metrics endpoint at /metrics
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)

    logger.info("Prometheus metrics enabled at /metrics endpoint")
    return instrumentator


def update_data_loader_metrics(data_loader):
    """
    Update Prometheus metrics with data loader statistics.

    Args:
        data_loader: DataLoader instance
    """
    try:
        data_loader_items.labels(data_type="provinces").set(len(data_loader.provinces))
        data_loader_items.labels(data_type="districts").set(len(data_loader.districts))
        data_loader_items.labels(data_type="neighborhoods").set(len(data_loader.neighborhoods))
        data_loader_items.labels(data_type="villages").set(len(data_loader.villages))
        data_loader_items.labels(data_type="towns").set(len(data_loader.towns))
        logger.debug("Updated data loader metrics")
    except Exception as e:
        logger.error(f"Failed to update data loader metrics: {e}")


def set_app_info(version: str, environment: str):
    """
    Set application information in Prometheus metrics.

    Args:
        version: Application version
        environment: Environment name (development, production, etc.)
    """
    try:
        app_info.info({"version": version, "environment": environment, "app_name": "Turkiye API"})
        logger.debug(f"Set app info: version={version}, environment={environment}")
    except Exception as e:
        logger.error(f"Failed to set app info: {e}")
