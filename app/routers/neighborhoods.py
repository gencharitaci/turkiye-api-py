import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query

from app.services.neighborhood_service import neighborhood_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/neighborhoods")
async def get_neighborhoods(
    name: Optional[str] = Query(None, description="The neighborhood name"),
    minPopulation: Optional[int] = Query(None, description="The minimum population of the neighborhood"),
    maxPopulation: Optional[int] = Query(None, description="The maximum population of the neighborhood"),
    provinceId: Optional[int] = Query(None, description="The province ID"),
    province: Optional[str] = Query(None, description="The province name"),
    districtId: Optional[int] = Query(None, description="The district ID"),
    district: Optional[str] = Query(None, description="The district name"),
    offset: int = Query(0, ge=0, le=100000, description="The offset of the neighborhoods list"),
    limit: int = Query(10000, ge=1, le=50000, description="The limit of the neighborhoods list"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    sort: Optional[str] = Query(
        None, description="The sorting of the neighborhoods list (put '-' before the field name for descending order)"
    ),
):
    try:
        neighborhoods = neighborhood_service.get_neighborhoods(
            name=name,
            min_population=minPopulation,
            max_population=maxPopulation,
            province_id=provinceId,
            province=province,
            district_id=districtId,
            district=district,
            offset=offset,
            limit=limit,
            fields=fields,
            sort=sort,
        )
        return {"status": "OK", "data": neighborhoods}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_neighborhoods")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/neighborhoods/{id}")
async def get_exact_neighborhood(
    id: int = Path(..., description="The neighborhood ID"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
):
    try:
        neighborhood = neighborhood_service.get_exact_neighborhood(neighborhood_id=id, fields=fields)
        return {"status": "OK", "data": neighborhood}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_exact_neighborhood")
        raise HTTPException(status_code=500, detail="Internal Server Error")
