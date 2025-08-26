from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    ReadingListItemData, ReadingListItemAttributes,
    ReadingListItemListJsonApiResponse, ReadingListItemJsonApiResponse
)
from .common import build_pagination_links

reading_list_item_router = APIRouter(
    tags=["ReadingListItem"],
    dependencies=[Depends(get_authenticated_user)]
)

@reading_list_item_router.get(
    "/reading-list-items", 
    response_model=ReadingListItemListJsonApiResponse,
    summary="All Reading List Items",
    responses={
        200: {
            "description": "List of reading list items",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "reading-list-items",
                                "attributes": {
                                    "list-id": 2,
                                    "status": "available",
                                    "hidden": False,
                                    "reading-id": 1,
                                    "reading-importance": "required",
                                    "reading-utilisations-count": 0,
                                    "usage-count": 0,
                                    "updated-at": "2019-01-16T12:36:43.000Z",
                                    "created-at": "2019-01-16T12:36:43.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/reading-list-items?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/reading-list-items?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/reading-list-items?page%5Bnumber%5D=86372&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_reading_list_items(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all reading list items in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("readingListItems", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    reading_list_item_data = []
    for reading_list_item in result["items"]:
        reading_list_item_attributes = ReadingListItemAttributes(
            list_id=reading_list_item["list_id"],
            reading_id=reading_list_item["reading_id"],
            status=reading_list_item["status"],
            hidden=reading_list_item["hidden"],
            reading_utilisations_count=reading_list_item["reading_utilisations_count"],
            reading_importance=reading_list_item["reading_importance"],
            usage_count=reading_list_item["usage_count"],
            created_at=reading_list_item.get("created_at", ""),
            updated_at=reading_list_item.get("updated_at", "")
        )
        reading_list_item_item = ReadingListItemData(
            id=str(reading_list_item["id"]),
            attributes=reading_list_item_attributes
        )
        reading_list_item_data.append(reading_list_item_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return ReadingListItemListJsonApiResponse(data=reading_list_item_data, links=links.dict(exclude_none=True))

@reading_list_item_router.get(
    "/reading-list-items/{id}", 
    response_model=ReadingListItemJsonApiResponse,
    summary="Find Reading List Item by ID",
    responses={
        200: {
            "description": "Reading list item details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "reading-list-items",
                            "attributes": {
                                "list-id": 3,
                                "status": "available",
                                "hidden": False,
                                "reading-id": 2,
                                "reading-importance": "required",
                                "reading-utilisations-count": 0,
                                "usage-count": 0,
                                "updated-at": "2019-01-16T12:36:45.000Z",
                                "created-at": "2019-01-16T12:36:45.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Reading list item not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in reading_list_items"
                        }]
                    }
                }
            }
        }
    }
)
async def get_reading_list_item(
    id: str = Path(..., description="Reading List Item ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific reading list item by ID in JSON API format'''
    reading_list_item = repo.get_by_id("readingListItems", id)
    
    # Convert to JSON API format
    reading_list_item_attributes = ReadingListItemAttributes(
        list_id=reading_list_item["list_id"],
        reading_id=reading_list_item["reading_id"],
        status=reading_list_item["status"],
        hidden=reading_list_item["hidden"],
        reading_utilisations_count=reading_list_item["reading_utilisations_count"],
        reading_importance=reading_list_item["reading_importance"],
        usage_count=reading_list_item["usage_count"],
        created_at=reading_list_item.get("created_at", ""),
        updated_at=reading_list_item.get("updated_at", "")
    )
    reading_list_item_data = ReadingListItemData(
        id=str(reading_list_item["id"]),
        attributes=reading_list_item_attributes
    )
    
    return ReadingListItemJsonApiResponse(data=reading_list_item_data)

router = reading_list_item_router