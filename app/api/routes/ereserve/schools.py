from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    SchoolData, SchoolAttributes,
    SchoolListJsonApiResponse, SchoolJsonApiResponse
)
from .common import build_pagination_links

school_router = APIRouter(
    tags=["School"],
    dependencies=[Depends(get_authenticated_user)]
)

@school_router.get(
    "/schools", 
    response_model=SchoolListJsonApiResponse,
    summary="All Schools",
    responses={
        200: {
            "description": "List of schools",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "schools",
                                "attributes": {
                                    "name": "School of Computer Science"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/schools?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/schools?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/schools?page%5Bnumber%5D=8&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)

async def all_schools(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all schools in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("schools", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    school_data = []
    for school in result["items"]:
        school_attributes = SchoolAttributes(name=school["name"])
        school_item = SchoolData(
            id=str(school["id"]),
            attributes=school_attributes
        )
        school_data.append(school_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return SchoolListJsonApiResponse(data=school_data, links=links.dict(exclude_none=True))

@school_router.get(
    "/schools/{id}", 
    response_model=SchoolJsonApiResponse,
    summary="Find school by ID",
    responses={
        200: {
            "description": "School details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "1",
                            "type": "schools",
                            "attributes": {
                                "name": "School of Computer Science"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "School not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in schools"
                        }]
                    }
                }
            }
        }
    }
)

async def get_school(
    id: str = Path(..., description="School ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific school by ID in JSON API format'''
    school = repo.get_by_id("schools", id)
    
    # Convert to JSON API format
    school_attributes = SchoolAttributes(name=school["name"])
    school_data = SchoolData(
        id=str(school["id"]),
        attributes=school_attributes
    )
    
    return SchoolJsonApiResponse(data=school_data)

router = school_router