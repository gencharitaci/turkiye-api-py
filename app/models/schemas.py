from typing import List, Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class Maps(BaseModel):
    googleMaps: str
    openStreetMap: str


class RegionName(BaseModel):
    en: str
    tr: str


class NUTS1Name(BaseModel):
    en: str
    tr: str


class NUTS1(BaseModel):
    code: str
    name: NUTS1Name


class NUTS2(BaseModel):
    code: str
    name: str


class NUTS(BaseModel):
    nuts1: NUTS1
    nuts2: NUTS2
    nuts3: str


class DistrictSummary(BaseModel):
    id: int
    name: str
    population: int
    area: int


class Province(BaseModel):
    id: int
    name: str
    population: int
    area: int
    altitude: int
    areaCode: List[int]
    isCoastal: bool
    isMetropolitan: bool
    nuts: NUTS
    coordinates: Coordinates
    maps: Maps
    region: RegionName
    districts: Optional[List[DistrictSummary]] = []
    postalCode: Optional[str] = None


class NeighborhoodSummary(BaseModel):
    id: int
    name: str
    population: int


class VillageSummary(BaseModel):
    id: int
    name: str
    population: int


class District(BaseModel):
    id: int
    provinceId: int
    province: str
    name: str
    population: int
    area: int
    postalCode: Optional[str] = None
    neighborhoods: Optional[List[NeighborhoodSummary]] = None
    villages: Optional[List[VillageSummary]] = None


class Neighborhood(BaseModel):
    id: int
    districtId: int
    provinceId: int
    district: str
    province: str
    name: str
    population: int


class Village(BaseModel):
    id: int
    districtId: int
    provinceId: int
    district: str
    province: str
    name: str
    population: int


class Town(BaseModel):
    id: int
    districtId: int
    provinceId: int
    district: str
    province: str
    name: str
    population: int


class APIResponse(BaseModel):
    status: str
    data: Optional[List | dict] = None


class ErrorResponse(BaseModel):
    status: str
    error: str
