import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.config import (
    DEFAULT_MAX_ALTITUDE,
    DEFAULT_MAX_AREA,
    DEFAULT_MAX_POPULATION,
    DEFAULT_MIN_ALTITUDE,
    DEFAULT_MIN_AREA,
    DEFAULT_MIN_POPULATION,
)
from app.services.base_service import BaseService
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)


class ProvinceService(BaseService):
    """Service for managing province data operations with caching support."""

    def __init__(self):
        super().__init__()
        self.cache = cache_service

    def get_provinces(
        self,
        name: Optional[str] = None,
        min_population: Optional[int] = None,
        max_population: Optional[int] = None,
        min_area: Optional[int] = None,
        max_area: Optional[int] = None,
        min_altitude: Optional[int] = None,
        max_altitude: Optional[int] = None,
        is_coastal: Optional[bool] = None,
        is_metropolitan: Optional[bool] = None,
        activate_postal_codes: bool = False,
        postal_code: Optional[str] = None,
        offset: int = 0,
        limit: int = 81,
        fields: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        # Try cache first
        cache_key = self.cache.generate_key(
            "provinces",
            name=name,
            min_pop=min_population,
            max_pop=max_population,
            min_area=min_area,
            max_area=max_area,
            min_alt=min_altitude,
            max_alt=max_altitude,
            coastal=is_coastal,
            metro=is_metropolitan,
            postal=activate_postal_codes,
            postal_code=postal_code,
            offset=offset,
            limit=limit,
            fields=fields,
            sort=sort,
        )

        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Returning cached provinces result ({len(cached_result)} items)")
            return cached_result

        # Get provinces (no .copy() needed - filtering creates new list)
        provinces = self.data_loader.provinces

        # Remove postal codes if not activated
        if not activate_postal_codes:
            provinces = [{k: v for k, v in p.items() if k != "postalCode"} for p in provinces]
        else:
            # Create shallow copy to avoid modifying original
            provinces = [p.copy() for p in provinces]

        # Add districts using pre-indexed lookups (O(1) instead of O(n*m))
        for province in provinces:
            province["districts"] = self.data_loader.districts_by_province.get(province["id"], [])

        if name:
            name_alt = name.capitalize()
            provinces = [p for p in provinces if name in p["name"] or name_alt in p["name"]]

        if min_population is not None and max_population is not None:
            if min_population <= 0 and max_population <= 0:
                raise HTTPException(
                    status_code=404, detail="You can't search for a province with a population of 0 or less."
                )
            if min_population > max_population:
                raise HTTPException(
                    status_code=404, detail="The minimum population cannot be greater than the maximum population."
                )

        if min_population is not None or max_population is not None:
            min_pop = min_population if min_population is not None else DEFAULT_MIN_POPULATION
            max_pop = max_population if max_population is not None else DEFAULT_MAX_POPULATION
            provinces = [p for p in provinces if min_pop <= p["population"] <= max_pop]

        if min_area is not None and max_area is not None:
            if min_area <= 0 and max_area <= 0:
                raise HTTPException(
                    status_code=404, detail="You can't search for a province with an area of 0 or less."
                )
            if min_area > max_area:
                raise HTTPException(status_code=404, detail="The minimum area cannot be greater than the maximum area.")

        if min_area is not None or max_area is not None:
            min_a = min_area if min_area is not None else DEFAULT_MIN_AREA
            max_a = max_area if max_area is not None else DEFAULT_MAX_AREA
            provinces = [p for p in provinces if min_a <= p["area"] <= max_a]

        if min_altitude is not None or max_altitude is not None:
            min_alt = min_altitude if min_altitude is not None else DEFAULT_MIN_ALTITUDE
            max_alt = max_altitude if max_altitude is not None else DEFAULT_MAX_ALTITUDE
            provinces = [p for p in provinces if min_alt <= p["altitude"] <= max_alt]

        if is_coastal is not None:
            provinces = [p for p in provinces if p["isCoastal"] == is_coastal]

        if is_metropolitan is not None:
            provinces = [p for p in provinces if p["isMetropolitan"] == is_metropolitan]

        if postal_code:
            provinces = [p for p in provinces if p.get("postalCode") and postal_code in p["postalCode"]]

        if not provinces:
            raise HTTPException(status_code=404, detail="Provinces not found.")

        provinces = self._sort_data(provinces, sort)

        len(provinces)
        provinces = provinces[offset : offset + limit]

        if fields:
            provinces = [self._filter_fields(p, fields) for p in provinces]

        # Cache result before returning (TTL: 30 minutes for query results)
        self.cache.set(cache_key, provinces, ttl=1800)

        return provinces

    def get_exact_province(
        self, province_id: int, fields: Optional[str] = None, extend: bool = False, activate_postal_codes: bool = False
    ) -> Dict[str, Any]:
        provinces = self.data_loader.provinces
        province = next((p for p in provinces if p["id"] == province_id), None)

        if not province:
            raise HTTPException(status_code=404, detail="Province not found.")

        # Create shallow copy to avoid modifying original
        province = province.copy()

        if not activate_postal_codes and "postalCode" in province:
            del province["postalCode"]

        # Use pre-indexed lookup for districts (O(1) instead of O(n))
        province["districts"] = self.data_loader.districts_by_province.get(province["id"], [])

        # If extend=true, add neighborhoods and villages using pre-indexed lookups
        if extend:
            for district in province["districts"]:
                # O(1) lookup instead of O(n) iteration
                district["neighborhoods"] = self.data_loader.neighborhoods_by_district.get(district["id"], [])
                district["villages"] = self.data_loader.villages_by_district.get(district["id"], [])

        if fields:
            province = self._filter_fields(province, fields)

        return province


province_service = ProvinceService()
