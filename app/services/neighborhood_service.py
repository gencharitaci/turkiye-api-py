import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.config import DEFAULT_MAX_POPULATION, DEFAULT_MIN_POPULATION
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)


class NeighborhoodService(BaseService):
    """Service for managing neighborhood data operations."""

    def __init__(self):
        super().__init__()

    def get_neighborhoods(
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
        # Get neighborhoods (no .copy() needed - filtering creates new list)
        neighborhoods = self.data_loader.neighborhoods

        if name:
            name_alt = name.capitalize()
            neighborhoods = [n for n in neighborhoods if name in n["name"] or name_alt in n["name"]]

        if min_population is not None or max_population is not None:
            min_pop = min_population if min_population is not None else DEFAULT_MIN_POPULATION
            max_pop = max_population if max_population is not None else DEFAULT_MAX_POPULATION
            neighborhoods = [n for n in neighborhoods if min_pop <= n["population"] <= max_pop]

        if province_id is not None:
            neighborhoods = [n for n in neighborhoods if n["provinceId"] == province_id]

        if province:
            province_alt = province.capitalize()
            neighborhoods = [n for n in neighborhoods if province in n["province"] or province_alt in n["province"]]

        if district_id is not None:
            neighborhoods = [n for n in neighborhoods if n["districtId"] == district_id]

        if district:
            district_alt = district.capitalize()
            neighborhoods = [n for n in neighborhoods if district in n["district"] or district_alt in n["district"]]

        if not neighborhoods:
            raise HTTPException(status_code=404, detail="Neighborhoods not found.")

        neighborhoods = self._sort_data(neighborhoods, sort)

        len(neighborhoods)
        neighborhoods = neighborhoods[offset : offset + limit]

        if fields:
            neighborhoods = [self._filter_fields(n, fields) for n in neighborhoods]

        return neighborhoods

    def get_exact_neighborhood(self, neighborhood_id: int, fields: Optional[str] = None) -> Dict[str, Any]:
        neighborhoods = self.data_loader.neighborhoods
        neighborhood = next((n for n in neighborhoods if n["id"] == neighborhood_id), None)

        if not neighborhood:
            raise HTTPException(status_code=404, detail="Neighborhood not found.")

        neighborhood = neighborhood.copy()

        if fields:
            neighborhood = self._filter_fields(neighborhood, fields)

        return neighborhood


neighborhood_service = NeighborhoodService()
