import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.config import DEFAULT_MAX_POPULATION, DEFAULT_MIN_POPULATION
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class TownService(BaseService):
    """Service for managing town data operations."""

    def __init__(self):
        super().__init__()

    def get_towns(
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
        # Get towns (no .copy() needed - filtering creates new list)
        towns = self.data_loader.towns

        if name:
            name_alt = name.capitalize()
            towns = [t for t in towns if name in t["name"] or name_alt in t["name"]]

        if min_population is not None or max_population is not None:
            min_pop = min_population if min_population is not None else DEFAULT_MIN_POPULATION
            max_pop = max_population if max_population is not None else DEFAULT_MAX_POPULATION
            towns = [t for t in towns if min_pop <= t["population"] <= max_pop]

        if province_id is not None:
            towns = [t for t in towns if t["provinceId"] == province_id]

        if province:
            province_alt = province.capitalize()
            towns = [t for t in towns if province in t["province"] or province_alt in t["province"]]

        if district_id is not None:
            towns = [t for t in towns if t["districtId"] == district_id]

        if district:
            district_alt = district.capitalize()
            towns = [t for t in towns if district in t["district"] or district_alt in t["district"]]

        if not towns:
            raise HTTPException(status_code=404, detail="Towns not found.")

        towns = self._sort_data(towns, sort)

        len(towns)
        towns = towns[offset : offset + limit]

        if fields:
            towns = [self._filter_fields(t, fields) for t in towns]

        return towns

    def get_exact_town(self, town_id: int, fields: Optional[str] = None) -> Dict[str, Any]:
        towns = self.data_loader.towns
        town = next((t for t in towns if t["id"] == town_id), None)

        if not town:
            raise HTTPException(status_code=404, detail="Town not found.")

        town = town.copy()

        if fields:
            town = self._filter_fields(town, fields)

        return town


town_service = TownService()
