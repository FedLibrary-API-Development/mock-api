from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    ReadingUtilisationData, ReadingUtilisationAttributes,
    ReadingUtilisationListJsonApiResponse, ReadingUtilisationJsonApiResponse
)
from .common import build_pagination_links

reading_utilisation_router = APIRouter(
    tags=["ReadingUtilisation"],
    dependencies=[Depends(get_authenticated_user)]
)

@reading_utilisation_router.get(
    "/reading-utilisations", 
    response_model=ReadingUtilisationListJsonApiResponse,
    summary="All Reading Utilisations",
    responses={
        200: {
            "description": "List of reading utilisations",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "reading-utilisations",
                                "attributes": {
                                    "item-id": 870,
                                    "item-usage-id": 1,
                                    "integration-user-id": 34,
                                    "created-at": "2019-01-30T11:47:23.000Z",
                                    "updated-at": "2019-01-30T11:47:23.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/reading-utilisations?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/reading-utilisations?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/reading-utilisations?page%5Bnumber%5D=717712&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_reading_utilisations(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all reading utilisations in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("readingUtilisations", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    reading_utilisation_data = []
    for reading_utilisation in result["items"]:
        reading_utilisation_attributes = ReadingUtilisationAttributes(
            item_id=reading_utilisation["item_id"],
            item_usage_id=reading_utilisation["item_usage_id"],
            integration_user_id=reading_utilisation["integration_user_id"],
            created_at=reading_utilisation.get("created_at", ""),
            updated_at=reading_utilisation.get("updated_at", "")
        )
        reading_utilisation_item = ReadingUtilisationData(
            id=str(reading_utilisation["id"]),
            attributes=reading_utilisation_attributes
        )
        reading_utilisation_data.append(reading_utilisation_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return ReadingUtilisationListJsonApiResponse(data=reading_utilisation_data, links=links.dict(exclude_none=True))

@reading_utilisation_router.get(
    "/reading-utilisations/{id}", 
    response_model=ReadingUtilisationJsonApiResponse,
    summary="Find Reading Utilisation by ID",
    responses={
        200: {
            "description": "Reading utilisation details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "reading-utilisations",
                            "attributes": {
                                "item-id": 866,
                                "item-usage-id": 2,
                                "integration-user-id": 25492,
                                "created-at": "2019-01-30T22:01:44.000Z",
                                "updated-at": "2019-01-30T22:01:44.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Reading utilisation not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 2 not found in reading_utilisations"
                        }]
                    }
                }
            }
        }
    }
)
async def get_reading_utilisation(
    id: str = Path(..., description="Reading Utilisation ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific reading utilisation by ID in JSON API format'''
    reading_utilisation = repo.get_by_id("readingUtilisations", id)
    
    # Convert to JSON API format
    reading_utilisation_attributes = ReadingUtilisationAttributes(
        item_id=reading_utilisation["item_id"],
        item_usage_id=reading_utilisation["item_usage_id"],
        integration_user_id=reading_utilisation["integration_user_id"],
        created_at=reading_utilisation.get("created_at", ""),
        updated_at=reading_utilisation.get("updated_at", "")
    )
    reading_utilisation_data = ReadingUtilisationData(
        id=str(reading_utilisation["id"]),
        attributes=reading_utilisation_attributes
    )
    
    return ReadingUtilisationJsonApiResponse(data=reading_utilisation_data)

router = reading_utilisation_router