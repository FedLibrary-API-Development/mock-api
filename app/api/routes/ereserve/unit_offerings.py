from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    UnitOfferingData, UnitOfferingAttributes,
    UnitOfferingListJsonApiResponse, UnitOfferingJsonApiResponse
)
from .common import build_pagination_links

unit_offering_router = APIRouter(
    tags=["UnitOffering"],
    dependencies=[Depends(get_authenticated_user)]
)

@unit_offering_router.get(
    "/unit-offerings", 
    response_model=UnitOfferingListJsonApiResponse,
    summary="All Unit Offerings",
    responses={
        200: {
            "description": "List of unit offerings",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "unit-offerings",
                                "attributes": {
                                    "unit-id": 1,
                                    "reading-list-id": None,
                                    "source-unit-code": "DeL Test Course",
                                    "source-unit-name": None,
                                    "source-unit-offering": None,
                                    "result": "no_match_found",
                                    "created-at": "2018-12-20T03:57:03.000Z",
                                    "updated-at": "2024-09-12T03:39:37.000Z",
                                    "list-publication-method": "auto"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/unit-offerings?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/unit-offerings?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/unit-offerings?page%5Bnumber%5D=4251&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_unit_offerings(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all unit offerings in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("unitOfferings", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    unit_offering_data = []
    for unit_offering in result["items"]:
        unit_offering_attributes = UnitOfferingAttributes(
            unit_id=unit_offering["unit_id"],
            reading_list_id=unit_offering.get("reading_list_id"),
            source_unit_code=unit_offering["source_unit_code"],
            source_unit_name=unit_offering.get("source_unit_name"),
            source_unit_offering=unit_offering.get("source_unit_offering"),
            result=unit_offering["result"],
            list_publication_method=unit_offering["list_publication_method"],
            created_at=unit_offering.get("created_at", ""),
            updated_at=unit_offering.get("updated_at", "")
        )
        unit_offering_item = UnitOfferingData(
            id=str(unit_offering["id"]),
            attributes=unit_offering_attributes
        )
        unit_offering_data.append(unit_offering_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return UnitOfferingListJsonApiResponse(data=unit_offering_data, links=links.dict(exclude_none=True))

@unit_offering_router.get(
    "/unit-offerings/{id}", 
    response_model=UnitOfferingJsonApiResponse,
    summary="Find Unit Offering by ID",
    responses={
        200: {
            "description": "Unit offering details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "unit-offerings",
                            "attributes": {
                                "unit-id": 2,
                                "reading-list-id": None,
                                "source-unit-code": "Master Shell BEHAV3004",
                                "source-unit-name": "Master Shell BEHAV3004",
                                "source-unit-offering": "Master Shell BEHAV3004",
                                "result": "no_match_found",
                                "created-at": "2018-12-20T04:16:51.000Z",
                                "updated-at": "2022-02-03T00:53:21.000Z",
                                "list-publication-method": "auto"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Unit offering not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in unit_offerings"
                        }]
                    }
                }
            }
        }
    }
)
async def get_unit_offering(
    id: str = Path(..., description="Unit Offering ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific unit offering by ID in JSON API format'''
    unit_offering = repo.get_by_id("unitOfferings", id)
    
    # Convert to JSON API format
    unit_offering_attributes = UnitOfferingAttributes(
        unit_id=unit_offering["unit_id"],
        reading_list_id=unit_offering.get("reading_list_id"),
        source_unit_code=unit_offering["source_unit_code"],
        source_unit_name=unit_offering.get("source_unit_name"),
        source_unit_offering=unit_offering.get("source_unit_offering"),
        result=unit_offering["result"],
        list_publication_method=unit_offering["list_publication_method"],
        created_at=unit_offering.get("created_at", ""),
        updated_at=unit_offering.get("updated_at", "")
    )
    unit_offering_data = UnitOfferingData(
        id=str(unit_offering["id"]),
        attributes=unit_offering_attributes
    )
    
    return UnitOfferingJsonApiResponse(data=unit_offering_data)

router = unit_offering_router