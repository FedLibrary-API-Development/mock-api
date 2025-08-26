from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    UnitData, UnitAttributes,
    UnitListJsonApiResponse, UnitJsonApiResponse
)
from .common import build_pagination_links

unit_router = APIRouter(
    tags=["Unit"],
    dependencies=[Depends(get_authenticated_user)]
)

@unit_router.get(
    "/units", 
    response_model=UnitListJsonApiResponse,
    summary="All Units",
    responses={
        200: {
            "description": "List of units",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "units",
                                "attributes": {
                                    "code": "DeL Test Course",
                                    "name": "DeL Test Course",
                                    "created-at": "2018-12-20T03:57:03.000Z",
                                    "updated-at": "2018-12-20T04:00:14.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/units?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/units?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/units?page%5Bnumber%5D=2603&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_units(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all units in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("units", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    unit_data = []
    for unit in result["items"]:
        unit_attributes = UnitAttributes(
            code=unit["code"],
            name=unit["name"],
            created_at=unit.get("created_at", ""),
            updated_at=unit.get("updated_at", "")
        )
        unit_item = UnitData(
            id=str(unit["id"]),
            attributes=unit_attributes
        )
        unit_data.append(unit_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return UnitListJsonApiResponse(data=unit_data, links=links.dict(exclude_none=True))

@unit_router.get(
    "/units/{id}", 
    response_model=UnitJsonApiResponse,
    summary="Find Unit by ID",
    responses={
        200: {
            "description": "Unit details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "1",
                            "type": "units",
                            "attributes": {
                                "code": "DeL Test Course",
                                "name": "DeL Test Course",
                                "created-at": "2018-12-20T03:57:03.000Z",
                                "updated-at": "2018-12-20T04:00:14.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Unit not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in units"
                        }]
                    }
                }
            }
        }
    }
)

async def get_unit(
    id: str = Path(..., description="Unit ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific unit by ID in JSON API format'''
    unit = repo.get_by_id("units", id)
    
    # Convert to JSON API format
    unit_attributes = UnitAttributes(
        code=unit["code"],
        name=unit["name"],
        created_at=unit.get("created_at", ""),
        updated_at=unit.get("updated_at", "")
    )
    unit_data = UnitData(
        id=str(unit["id"]),
        attributes=unit_attributes
    )
    
    return UnitJsonApiResponse(data=unit_data)

router = unit_router