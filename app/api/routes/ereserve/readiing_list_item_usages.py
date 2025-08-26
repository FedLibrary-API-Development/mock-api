from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    ReadingListItemUsageData, ReadingListItemUsageAttributes,
    ReadingListItemUsageListJsonApiResponse, ReadingListItemUsageJsonApiResponse
)
from .common import build_pagination_links

reading_list_item_usage_router = APIRouter(
    tags=["ReadingListItemUsage"],
    dependencies=[Depends(get_authenticated_user)]
)

@reading_list_item_usage_router.get(
    "/reading-list-item-usages", 
    response_model=ReadingListItemUsageListJsonApiResponse,
    summary="All Reading List Item Usages",
    responses={
        200: {
            "description": "List of reading list item usages",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "reading-list-item-usages",
                                "attributes": {
                                    "item-id": 870,
                                    "list-usage-id": 1,
                                    "integration-user-id": 34,
                                    "utilisation-count": 1,
                                    "updated-at": "2019-01-30T11:47:23.000Z",
                                    "created-at": "2019-01-30T11:47:23.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/reading-list-item-usages?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/reading-list-item-usages?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/reading-list-item-usages?page%5Bnumber%5D=430009&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_reading_list_item_usages(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all reading list item usages in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("readingListItemUsages", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    reading_list_item_usage_data = []
    for reading_list_item_usage in result["items"]:
        reading_list_item_usage_attributes = ReadingListItemUsageAttributes(
            item_id=reading_list_item_usage["item_id"],
            list_usage_id=reading_list_item_usage["list_usage_id"],
            integration_user_id=reading_list_item_usage["integration_user_id"],
            utilisation_count=reading_list_item_usage["utilisation_count"],
            created_at=reading_list_item_usage.get("created_at", ""),
            updated_at=reading_list_item_usage.get("updated_at", "")
        )
        reading_list_item_usage_item = ReadingListItemUsageData(
            id=str(reading_list_item_usage["id"]),
            attributes=reading_list_item_usage_attributes
        )
        reading_list_item_usage_data.append(reading_list_item_usage_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return ReadingListItemUsageListJsonApiResponse(data=reading_list_item_usage_data, links=links.dict(exclude_none=True))

@reading_list_item_usage_router.get(
    "/reading-list-item-usages/{id}", 
    response_model=ReadingListItemUsageJsonApiResponse,
    summary="Find Reading List Item Usage by ID",
    responses={
        200: {
            "description": "Reading list item usage details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "reading-list-item-usages",
                            "attributes": {
                                "item-id": 866,
                                "list-usage-id": 2,
                                "integration-user-id": 25492,
                                "utilisation-count": 2,
                                "updated-at": "2019-01-31T20:22:38.000Z",
                                "created-at": "2019-01-30T22:01:44.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Reading list item usage not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in reading_list_item_usages"
                        }]
                    }
                }
            }
        }
    }
)
async def get_reading_list_item_usage(
    id: str = Path(..., description="Reading List Item Usage ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific reading list item usage by ID in JSON API format'''
    reading_list_item_usage = repo.get_by_id("readingListItemUsages", id)
    
    # Convert to JSON API format
    reading_list_item_usage_attributes = ReadingListItemUsageAttributes(
        item_id=reading_list_item_usage["item_id"],
        list_usage_id=reading_list_item_usage["list_usage_id"],
        integration_user_id=reading_list_item_usage["integration_user_id"],
        utilisation_count=reading_list_item_usage["utilisation_count"],
        created_at=reading_list_item_usage.get("created_at", ""),
        updated_at=reading_list_item_usage.get("updated_at", "")
    )
    reading_list_item_usage_data = ReadingListItemUsageData(
        id=str(reading_list_item_usage["id"]),
        attributes=reading_list_item_usage_attributes
    )
    
    return ReadingListItemUsageJsonApiResponse(data=reading_list_item_usage_data)

router = reading_list_item_usage_router