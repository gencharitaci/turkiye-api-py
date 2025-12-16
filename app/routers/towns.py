import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query

from app.services.town_service import town_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/towns")
async def get_towns(
    name: Optional[str] = Query(None, description="The town name"),
    minPopulation: Optional[int] = Query(None, description="The minimum population of the town"),
    maxPopulation: Optional[int] = Query(None, description="The maximum population of the town"),
    provinceId: Optional[int] = Query(None, description="The province ID"),
    province: Optional[str] = Query(None, description="The province name"),
    districtId: Optional[int] = Query(None, description="The district ID"),
    district: Optional[str] = Query(None, description="The district name"),
    offset: int = Query(0, ge=0, le=100000, description="The offset of the towns list"),
    limit: int = Query(10000, ge=1, le=10000, description="The limit of the towns list"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    sort: Optional[str] = Query(
        None, description="The sorting of the towns list (put '-' before the field name for descending order)"
    ),
):
    try:
        towns = town_service.get_towns(
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
        return {"status": "OK", "data": towns}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_towns")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/towns/{id}")
async def get_exact_town(
    id: int = Path(..., description="The town ID"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
):
    try:
        town = town_service.get_exact_town(town_id=id, fields=fields)
        return {"status": "OK", "data": town}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_exact_town")
        raise HTTPException(status_code=500, detail="Internal Server Error")
