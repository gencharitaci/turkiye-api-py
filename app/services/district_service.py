import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.config import DEFAULT_MAX_AREA, DEFAULT_MAX_POPULATION, DEFAULT_MIN_AREA, DEFAULT_MIN_POPULATION
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class DistrictService(BaseService):
    """Service for managing district data operations."""

    def __init__(self):
        super().__init__()

    def get_districts(
        self,
        name: Optional[str] = None,
        min_population: Optional[int] = None,
        max_population: Optional[int] = None,
        min_area: Optional[int] = None,
        max_area: Optional[int] = None,
        province_id: Optional[int] = None,
        province: Optional[str] = None,
        activate_postal_codes: bool = False,
        postal_code: Optional[str] = None,
        offset: int = 0,
        limit: int = 1000,
        fields: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        # Get districts (no .copy() needed - filtering creates new list)
        districts = self.data_loader.districts

        # Remove postal codes if not activated
        if not activate_postal_codes:
            districts = [{k: v for k, v in d.items() if k != "postalCode"} for d in districts]
        else:
            # Create shallow copy to avoid modifying original
            districts = [d.copy() for d in districts]

        if name:
            name_alt = name.capitalize()
            districts = [d for d in districts if name in d["name"] or name_alt in d["name"]]

        if min_population is not None or max_population is not None:
            min_pop = min_population if min_population is not None else DEFAULT_MIN_POPULATION
            max_pop = max_population if max_population is not None else DEFAULT_MAX_POPULATION
            districts = [d for d in districts if min_pop <= d["population"] <= max_pop]

        if min_area is not None or max_area is not None:
            min_a = min_area if min_area is not None else DEFAULT_MIN_AREA
            max_a = max_area if max_area is not None else DEFAULT_MAX_AREA
            districts = [d for d in districts if min_a <= d["area"] <= max_a]

        if province_id is not None:
            districts = [d for d in districts if d["provinceId"] == province_id]

        if province:
            province_alt = province.capitalize()
            districts = [d for d in districts if province in d["province"] or province_alt in d["province"]]

        if postal_code:
            districts = [d for d in districts if d.get("postalCode") and postal_code in d["postalCode"]]

        if not districts:
            raise HTTPException(status_code=404, detail="Districts not found.")

        districts = self._sort_data(districts, sort)

        len(districts)
        districts = districts[offset : offset + limit]

        if fields:
            districts = [self._filter_fields(d, fields) for d in districts]

        return districts

    def get_exact_district(
        self, district_id: int, fields: Optional[str] = None, activate_postal_codes: bool = False
    ) -> Dict[str, Any]:
        districts = self.data_loader.districts
        district = next((d for d in districts if d["id"] == district_id), None)

        if not district:
            raise HTTPException(status_code=404, detail="District not found.")

        district = district.copy()

        if not activate_postal_codes and "postalCode" in district:
            del district["postalCode"]

        district_neighborhoods = [
            {"id": n["id"], "name": n["name"], "population": n["population"]}
            for n in self.data_loader.neighborhoods
            if n["districtId"] == district["id"]
        ]
        district["neighborhoods"] = district_neighborhoods

        district_villages = [
            {"id": v["id"], "name": v["name"], "population": v["population"]}
            for v in self.data_loader.villages
            if v["districtId"] == district["id"]
        ]
        district["villages"] = district_villages

        if fields:
            district = self._filter_fields(district, fields)

        return district


district_service = DistrictService()
