from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    ReadingListUsageData, ReadingListUsageAttributes,
    ReadingListUsageListJsonApiResponse, ReadingListUsageJsonApiResponse
)
from .common import build_pagination_links

reading_list_usage_router = APIRouter(
    tags=["ReadingListUsage"],
    dependencies=[Depends(get_authenticated_user)]
)

@reading_list_usage_router.get(
    "/reading-list-usages", 
    response_model=ReadingListUsageListJsonApiResponse,
    summary="All Reading List Usages",
    responses={
        200: {
            "description": "List of reading list usages",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "reading-list-usages",
                                "attributes": {
                                    "list-id": 130,
                                    "integration-user-id": 34,
                                    "item-usage-count": 9,
                                    "updated-at": "2019-02-24T07:56:48.000Z",
                                    "created-at": "2019-01-30T11:47:23.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/reading-list-usages?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/reading-list-usages?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/reading-list-usages?page%5Bnumber%5D=63373&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_reading_list_usages(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all reading list usages in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("readingListUsages", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    reading_list_usage_data = []
    for reading_list_usage in result["items"]:
        reading_list_usage_attributes = ReadingListUsageAttributes(
            list_id=reading_list_usage["list_id"],
            integration_user_id=reading_list_usage["integration_user_id"],
            item_usage_count=reading_list_usage["item_usage_count"],
            created_at=reading_list_usage.get("created_at", ""),
            updated_at=reading_list_usage.get("updated_at", "")
        )
        reading_list_usage_item = ReadingListUsageData(
            id=str(reading_list_usage["id"]),
            attributes=reading_list_usage_attributes
        )
        reading_list_usage_data.append(reading_list_usage_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return ReadingListUsageListJsonApiResponse(data=reading_list_usage_data, links=links.dict(exclude_none=True))

@reading_list_usage_router.get(
    "/reading-list-usages/{id}", 
    response_model=ReadingListUsageJsonApiResponse,
    summary="Find Reading List Usage by ID",
    responses={
        200: {
            "description": "Reading list usage details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "reading-list-usages",
                            "attributes": {
                                "list-id": 130,
                                "integration-user-id": 25492,
                                "item-usage-count": 8,
                                "updated-at": "2019-01-31T20:11:55.000Z",
                                "created-at": "2019-01-30T22:01:44.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Reading list usage not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in readingListUsages"
                        }]
                    }
                }
            }
        }
    }
)
async def get_reading_list_usage(
    id: str = Path(..., description="Reading List Usage ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific reading list usage by ID in JSON API format'''
    reading_list_usage = repo.get_by_id("readingListUsages", id)
    
    # Convert to JSON API format
    reading_list_usage_attributes = ReadingListUsageAttributes(
        list_id=reading_list_usage["list_id"],
        integration_user_id=reading_list_usage["integration_user_id"],
        item_usage_count=reading_list_usage["item_usage_count"],
        created_at=reading_list_usage.get("created_at", ""),
        updated_at=reading_list_usage.get("updated_at", "")
    )
    reading_list_usage_data = ReadingListUsageData(
        id=str(reading_list_usage["id"]),
        attributes=reading_list_usage_attributes
    )
    
    return ReadingListUsageJsonApiResponse(data=reading_list_usage_data)

router = reading_list_usage_router