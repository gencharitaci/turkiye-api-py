import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query

from app.services.province_service import province_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/provinces")
async def get_provinces(
    name: Optional[str] = Query(None, description="The province name"),
    minPopulation: Optional[int] = Query(None, description="The minimum population of the province"),
    maxPopulation: Optional[int] = Query(None, description="The maximum population of the province"),
    minArea: Optional[int] = Query(None, description="The minimum area of the province"),
    maxArea: Optional[int] = Query(None, description="The maximum area of the province"),
    minAltitude: Optional[int] = Query(None, description="The minimum altitude of the province"),
    maxAltitude: Optional[int] = Query(None, description="The maximum altitude of the province"),
    isCoastal: Optional[bool] = Query(None, description="The province is coastal or not"),
    isMetropolitan: Optional[bool] = Query(None, description="The province is metropolitan or not"),
    activatePostalCodes: bool = Query(False, description="Activate postal codes"),
    postalCode: Optional[str] = Query(None, description="Filter by postal code"),
    offset: int = Query(0, ge=0, le=100000, description="The offset of the provinces list"),
    limit: int = Query(81, ge=1, le=1000, description="The limit of the provinces list"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    sort: Optional[str] = Query(
        None, description="The sorting of the provinces list (put '-' before the field name for descending order)"
    ),
):
    try:
        provinces = province_service.get_provinces(
            name=name,
            min_population=minPopulation,
            max_population=maxPopulation,
            min_area=minArea,
            max_area=maxArea,
            min_altitude=minAltitude,
            max_altitude=maxAltitude,
            is_coastal=isCoastal,
            is_metropolitan=isMetropolitan,
            activate_postal_codes=activatePostalCodes,
            postal_code=postalCode,
            offset=offset,
            limit=limit,
            fields=fields,
            sort=sort,
        )
        return {"status": "OK", "data": provinces}
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Unexpected error in get_provinces")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/provinces/{id}")
async def get_exact_province(
    id: int = Path(..., description="The province ID / plate number"),
    fields: Optional[str] = Query(None, description="The fields to be returned (comma separated)"),
    extend: bool = Query(False, description="Extend the response with additional data (neighborhoods and villages)"),
    activatePostalCodes: bool = Query(False, description="Activate postal codes"),
):
    try:
        province = province_service.get_exact_province(
            province_id=id, fields=fields, extend=extend, activate_postal_codes=activatePostalCodes
        )
        return {"status": "OK", "data": province}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
