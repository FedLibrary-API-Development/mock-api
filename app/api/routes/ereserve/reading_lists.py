from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    ReadingListData, ReadingListAttributes,
    ReadingListListJsonApiResponse, ReadingListJsonApiResponse
)
from .common import build_pagination_links

reading_list_router = APIRouter(
    tags=["ReadingList"],
    dependencies=[Depends(get_authenticated_user)]
)

@reading_list_router.get(
    "/reading-lists", 
    response_model=ReadingListListJsonApiResponse,
    summary="All Reading Lists",
    responses={
        200: {
            "description": "List of reading lists",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "reading-lists",
                                "attributes": {
                                    "unit-id": 4,
                                    "teaching-session-id": 7,
                                    "name": "1902 SEM6 2019 Late Summer",
                                    "duration": "predefined",
                                    "start-date": "2018-12-10",
                                    "end-date": "2019-03-15",
                                    "hidden": False,
                                    "item-count": 0,
                                    "approved-item-count": 0,
                                    "usage-count": 0,
                                    "deleted": False,
                                    "updated-at": "2018-12-21T05:11:53.000Z",
                                    "created-at": "2018-12-21T05:11:53.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/reading-lists?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/reading-lists?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/reading-lists?page%5Bnumber%5D=2834&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_reading_lists(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all reading lists in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("readingLists", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    reading_list_data = []
    for reading_list in result["items"]:
        reading_list_attributes = ReadingListAttributes(
            unit_id=reading_list["unit_id"],
            teaching_session_id=reading_list.get("teaching_session_id"),
            name=reading_list["name"],
            duration=reading_list["duration"],
            start_date=reading_list["start_date"],
            end_date=reading_list["end_date"],
            hidden=reading_list["hidden"],
            item_count=reading_list["item_count"],
            approved_item_count=reading_list["approved_item_count"],
            usage_count=reading_list["usage_count"],
            deleted=reading_list["deleted"],
            created_at=reading_list.get("created_at", ""),
            updated_at=reading_list.get("updated_at", "")
        )
        reading_list_item = ReadingListData(
            id=str(reading_list["id"]),
            attributes=reading_list_attributes
        )
        reading_list_data.append(reading_list_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return ReadingListListJsonApiResponse(data=reading_list_data, links=links.dict(exclude_none=True))

@reading_list_router.get(
    "/reading-lists/{id}", 
    response_model=ReadingListJsonApiResponse,
    summary="Find Reading List by ID",
    responses={
        200: {
            "description": "Reading list details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "1",
                            "type": "reading-lists",
                            "attributes": {
                                "unit-id": 4,
                                "teaching-session-id": 7,
                                "name": "1902 SEM6 2019 Late Summer",
                                "duration": "predefined",
                                "start-date": "2018-12-10",
                                "end-date": "2019-03-15",
                                "hidden": False,
                                "item-count": 0,
                                "approved-item-count": 0,
                                "usage-count": 0,
                                "deleted": False,
                                "updated-at": "2018-12-21T05:11:53.000Z",
                                "created-at": "2018-12-21T05:11:53.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Reading list not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 1 not found in readingLists"
                        }]
                    }
                }
            }
        }
    }
)
async def get_reading_list(
    id: str = Path(..., description="Reading List ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific reading list by ID in JSON API format'''
    reading_list = repo.get_by_id("readingLists", id)
    
    # Convert to JSON API format
    reading_list_attributes = ReadingListAttributes(
        unit_id=reading_list["unit_id"],
        teaching_session_id=reading_list.get("teaching_session_id"),
        name=reading_list["name"],
        duration=reading_list["duration"],
        start_date=reading_list["start_date"],
        end_date=reading_list["end_date"],
        hidden=reading_list["hidden"],
        item_count=reading_list["item_count"],
        approved_item_count=reading_list["approved_item_count"],
        usage_count=reading_list["usage_count"],
        deleted=reading_list["deleted"],
        created_at=reading_list.get("created_at", ""),
        updated_at=reading_list.get("updated_at", "")
    )
    reading_list_data = ReadingListData(
        id=str(reading_list["id"]),
        attributes=reading_list_attributes
    )
    
    return ReadingListJsonApiResponse(data=reading_list_data)

router = reading_list_router