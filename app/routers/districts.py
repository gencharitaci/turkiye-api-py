import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query

from app.services.district_service import district_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/districts")
async def get_districts(
    name: Optional[str] = Query(None, description="The district name"),
    minPopulation: Optional[int] = Query(None, description="The minimum population of the district"),
    maxPopulation: Optional[int] = Query(None, description="The maximum population of the district"),
    minArea: Optional[int] = Query(None, description="The minimum area of the district"),
    maxArea: Optional[int] = Query(None, description="The maximum area of the district"),
    provinceId: Optional[int] = Query(None, description="The province ID"),
    province: Optional[str] = Query(None, description="The province name"),
    activatePostalCodes: bool = Query(False, description="Activate postal codes"),
    postalCode: Optional[str] = Query(None, description="Filter by postal code"),
    offset: int = Query(0, ge=0, le=100000, description="The offset of the districts list"),
    limit: int = Query(1000, ge=1, le=1000, description="The limit of the districts list"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    sort: Optional[str] = Query(
        None, description="The sorting of the districts list (put '-' before the field name for descending order)"
    ),
):
    try:
        districts = district_service.get_districts(
            name=name,
            min_population=minPopulation,
            max_population=maxPopulation,
            min_area=minArea,
            max_area=maxArea,
            province_id=provinceId,
            province=province,
            activate_postal_codes=activatePostalCodes,
            postal_code=postalCode,
            offset=offset,
            limit=limit,
            fields=fields,
            sort=sort,
        )
        return {"status": "OK", "data": districts}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_districts")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/districts/{id}")
async def get_exact_district(
    id: int = Path(..., description="The district ID"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    activatePostalCodes: bool = Query(False, description="Activate postal codes"),
):
    try:
        district = district_service.get_exact_district(
            district_id=id, fields=fields, activate_postal_codes=activatePostalCodes
        )
        return {"status": "OK", "data": district}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_exact_district")
        raise HTTPException(status_code=500, detail="Internal Server Error")
