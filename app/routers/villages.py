import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query

from app.services.village_service import village_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/villages")
async def get_villages(
    name: Optional[str] = Query(None, description="The village name"),
    minPopulation: Optional[int] = Query(None, description="The minimum population of the village"),
    maxPopulation: Optional[int] = Query(None, description="The maximum population of the village"),
    provinceId: Optional[int] = Query(None, description="The province ID"),
    province: Optional[str] = Query(None, description="The province name"),
    districtId: Optional[int] = Query(None, description="The district ID"),
    district: Optional[str] = Query(None, description="The district name"),
    offset: int = Query(0, ge=0, le=100000, description="The offset of the villages list"),
    limit: int = Query(10000, ge=1, le=50000, description="The limit of the villages list"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    sort: Optional[str] = Query(
        None, description="The sorting of the villages list (put '-' before the field name for descending order)"
    ),
):
    try:
        villages = village_service.get_villages(
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
        return {"status": "OK", "data": villages}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_villages")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/villages/{id}")
async def get_exact_village(
    id: int = Path(..., description="The village ID"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
):
    try:
        village = village_service.get_exact_village(village_id=id, fields=fields)
        return {"status": "OK", "data": village}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_exact_village")
        raise HTTPException(status_code=500, detail="Internal Server Error")
