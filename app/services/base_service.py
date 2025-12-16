"""
Base service class with shared utility methods for all services.

This module provides common functionality for filtering, sorting,
and validating data across all service classes.
"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.services.data_loader import data_loader

logger = logging.getLogger(__name__)


class BaseService:
    """Base service with shared utility methods for data operations."""

    def __init__(self):
        """Initialize base service with data loader."""
        self.data_loader = data_loader

    def _filter_fields(self, item: Dict[str, Any], fields: Optional[str]) -> Dict[str, Any]:
        """
        Filter item to include only specified fields.

        Args:
            item: Dictionary to filter
            fields: Comma-separated list of field names to include

        Returns:
            Dictionary with only the specified fields
        """
        if not fields:
            return item

        field_list = [f.strip() for f in fields.split(",")]
        return {k: v for k, v in item.items() if k in field_list}

    def _sort_data(self, data: List[Dict], sort: Optional[str]) -> List[Dict]:
        """
        Sort data by specified field.

        Args:
            data: List of dictionaries to sort
            sort: Field name to sort by. Prefix with '-' for descending order.

        Returns:
            Sorted list of dictionaries

        Raises:
            HTTPException: If sort field is invalid or not found in data
        """
        if not sort:
            return data

        reverse = sort.startswith("-")
        field = sort[1:] if reverse else sort

        # Validate field exists in data
        if data and field not in data[0]:
            logger.warning(f"Sort field '{field}' not found in data. Available fields: {list(data[0].keys())}")
            raise HTTPException(
                status_code=400, detail=f"Invalid sort field '{field}'. Field does not exist in the data."
            )

        try:
            return sorted(data, key=lambda x: x.get(field, 0), reverse=reverse)
        except (TypeError, KeyError) as e:
            logger.error(f"Sort error on field '{field}': {e}")
            raise HTTPException(
                status_code=400, detail=f"Cannot sort by field '{field}': invalid field type for sorting"
            )

    def validate_pagination(self, offset: int, limit: int, max_limit: int, max_offset: int = 100000) -> tuple[int, int]:
        """
        Validate and clamp pagination parameters.

        Args:
            offset: Starting position in the result set
            limit: Maximum number of items to return
            max_limit: Maximum allowed limit for this resource type
            max_offset: Maximum allowed offset (default: 100000)

        Returns:
            Tuple of (validated_offset, validated_limit)

        Raises:
            HTTPException: If pagination parameters are invalid
        """
        # Validate offset
        if offset < 0:
            raise HTTPException(status_code=400, detail="offset must be greater than or equal to 0")

        if offset > max_offset:
            raise HTTPException(status_code=400, detail=f"offset must be less than or equal to {max_offset}")

        # Validate limit
        if limit < 1:
            raise HTTPException(status_code=400, detail="limit must be greater than or equal to 1")

        # Clamp limit to max (with warning, not error)
        if limit > max_limit:
            logger.warning(f"Requested limit {limit} exceeds maximum {max_limit}, clamping to {max_limit}")
            limit = max_limit

        return offset, limit
