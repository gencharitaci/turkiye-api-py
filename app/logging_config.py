"""
Structured logging configuration for production-grade observability.

This module configures JSON-based structured logging for the application,
making logs machine-parseable for analysis tools like Elasticsearch, Datadog, etc.
"""

import logging
import os
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None, environment: Optional[str] = None) -> logging.Logger:
    """
    Configure structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               If None, uses LOG_LEVEL environment variable or defaults to INFO.
        environment: Environment name (development, production).
               If None, uses ENVIRONMENT environment variable or defaults to development.

    Returns:
        Configured root logger instance
    """
    # Determine log level
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Determine environment
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    if environment == "production":
        # JSON format for production (machine-parseable)
        try:
            from pythonjsonlogger import jsonlogger

            formatter = jsonlogger.JsonFormatter(
                "%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s",
                rename_fields={"asctime": "timestamp", "levelname": "level", "funcName": "function", "lineno": "line"},
                timestamp=True,
            )
        except ImportError:
            # Fallback to standard format if python-json-logger not installed
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            logger.warning(
                "python-json-logger not installed. "
                "Install with 'pip install python-json-logger' for structured logging."
            )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)d - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Log startup message
    logger.info(
        f"Logging configured: level={level}, environment={environment}, "
        f"format={'JSON' if environment == 'production' else 'text'}"
    )

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the module (typically __name__)

    Returns:
        Logger instance for the module
    """
    return logging.getLogger(name)
