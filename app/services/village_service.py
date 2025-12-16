import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.config import DEFAULT_MAX_POPULATION, DEFAULT_MIN_POPULATION
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class VillageService(BaseService):
    """Service for managing village data operations."""

    def __init__(self):
        super().__init__()

    def get_villages(
        self,
        name: Optional[str] = None,
        min_population: Optional[int] = None,
        max_population: Optional[int] = None,
        province_id: Optional[int] = None,
        province: Optional[str] = None,
        district_id: Optional[int] = None,
        district: Optional[str] = None,
        offset: int = 0,
        limit: int = 10000,
        fields: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        # Get villages (no .copy() needed - filtering creates new list)
        villages = self.data_loader.villages

        if name:
            name_alt = name.capitalize()
            villages = [v for v in villages if name in v["name"] or name_alt in v["name"]]

        if min_population is not None or max_population is not None:
            min_pop = min_population if min_population is not None else DEFAULT_MIN_POPULATION
            max_pop = max_population if max_population is not None else DEFAULT_MAX_POPULATION
            villages = [v for v in villages if min_pop <= v["population"] <= max_pop]

        if province_id is not None:
            villages = [v for v in villages if v["provinceId"] == province_id]

        if province:
            province_alt = province.capitalize()
            villages = [v for v in villages if province in v["province"] or province_alt in v["province"]]

        if district_id is not None:
            villages = [v for v in villages if v["districtId"] == district_id]

        if district:
            district_alt = district.capitalize()
            villages = [v for v in villages if district in v["district"] or district_alt in v["district"]]

        if not villages:
            raise HTTPException(status_code=404, detail="Villages not found.")

        villages = self._sort_data(villages, sort)

        len(villages)
        villages = villages[offset : offset + limit]

        if fields:
            villages = [self._filter_fields(v, fields) for v in villages]

        return villages

    def get_exact_village(self, village_id: int, fields: Optional[str] = None) -> Dict[str, Any]:
        villages = self.data_loader.villages
        village = next((v for v in villages if v["id"] == village_id), None)

        if not village:
            raise HTTPException(status_code=404, detail="Village not found.")

        village = village.copy()

        if fields:
            village = self._filter_fields(village, fields)

        return village


village_service = VillageService()
