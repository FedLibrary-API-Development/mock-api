from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    TeachingSessionData, TeachingSessionAttributes,
    TeachingSessionListJsonApiResponse, TeachingSessionJsonApiResponse
)
from .common import build_pagination_links

teaching_session_router = APIRouter(
    tags=["TeachingSession"],
    dependencies=[Depends(get_authenticated_user)]
)

@teaching_session_router.get(
    "/teaching-sessions", 
    response_model=TeachingSessionListJsonApiResponse,
    summary="All Teaching Sessions",
    responses={
        200: {
            "description": "List of teaching sessions",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "teaching-sessions",
                                "attributes": {
                                    "name": "1825 SEM5 2018 Spring (Cont. from 2018)",
                                    "start-date": "2018-08-04",
                                    "end-date": "2019-01-24",
                                    "archived": True,
                                    "created-at": "2018-09-19T01:54:32.000Z",
                                    "updated-at": "2019-12-17T22:52:45.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/teaching-sessions?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/teaching-sessions?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/teaching-sessions?page%5Bnumber%5D=48&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_teaching_sessions(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all teaching sessions in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("teachingSessions", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    teaching_session_data = []
    for teaching_session in result["items"]:
        teaching_session_attributes = TeachingSessionAttributes(
            name=teaching_session["name"],
            start_date=teaching_session["start_date"],
            end_date=teaching_session["end_date"],
            archived=teaching_session["archived"],
            created_at=teaching_session.get("created_at", ""),
            updated_at=teaching_session.get("updated_at", "")
        )
        teaching_session_item = TeachingSessionData(
            id=str(teaching_session["id"]),
            attributes=teaching_session_attributes
        )
        teaching_session_data.append(teaching_session_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return TeachingSessionListJsonApiResponse(data=teaching_session_data, links=links.dict(exclude_none=True))

@teaching_session_router.get(
    "/teaching-sessions/{id}", 
    response_model=TeachingSessionJsonApiResponse,
    summary="Find Teaching Session by ID",
    responses={
        200: {
            "description": "Teaching session details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "teaching-sessions",
                            "attributes": {
                                "name": "1901 SEM0 2019 VET Full Year",
                                "start-date": "2019-01-01",
                                "end-date": "2019-12-31",
                                "archived": True,
                                "created-at": "2018-09-19T01:55:31.000Z",
                                "updated-at": "2020-03-02T00:19:53.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Teaching session not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 2 not found in teaching_sessions"
                        }]
                    }
                }
            }
        }
    }
)
async def get_teaching_session(
    id: str = Path(..., description="Teaching Session ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific teaching session by ID in JSON API format'''
    teaching_session = repo.get_by_id("teachingSessions", id)
    
    # Convert to JSON API format
    teaching_session_attributes = TeachingSessionAttributes(
        name=teaching_session["name"],
        start_date=teaching_session["start_date"],
        end_date=teaching_session["end_date"],
        archived=teaching_session["archived"],
        created_at=teaching_session.get("created_at", ""),
        updated_at=teaching_session.get("updated_at", "")
    )
    teaching_session_data = TeachingSessionData(
        id=str(teaching_session["id"]),
        attributes=teaching_session_attributes
    )
    
    return TeachingSessionJsonApiResponse(data=teaching_session_data)

router = teaching_session_router