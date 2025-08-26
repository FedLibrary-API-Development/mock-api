from fastapi import APIRouter, Depends, Query, Path, Request

from app.db import EReserveRepository
from app.api.dependencies import get_ereserve_repository, get_authenticated_user
from app.schemas.ereserve import (
    IntegrationUserData, IntegrationUserAttributes,
    IntegrationUserListJsonApiResponse, IntegrationUserJsonApiResponse
)
from .common import build_pagination_links

integration_user_router = APIRouter(
    tags=["IntegrationUser"],
    dependencies=[Depends(get_authenticated_user)]
)

@integration_user_router.get(
    "/integration-users", 
    response_model=IntegrationUserListJsonApiResponse,
    summary="All Integration Users",
    responses={
        200: {
            "description": "List of integration users",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": [
                            {
                                "id": "1",
                                "type": "integration-users",
                                "attributes": {
                                    "identifier": "aalagesan",
                                    "roles": "Administrator",
                                    "first-name": "Albi",
                                    "last-name": "Alagesan",
                                    "email": "a.alagesan@federation.edu.au",
                                    "lti-consumer-user-id": "115826",
                                    "lti-lis-person-sourcedid": "Aalagesan",
                                    "created-at": "2018-12-20T03:57:03.000Z",
                                    "updated-at": "2022-07-26T10:06:59.000Z"
                                }
                            }
                        ],
                        "links": {
                            "first": "https://example.com/api/v1/integration-users?page%5Bnumber%5D=1&page%5Bsize%5D=2",
                            "next": "https://example.com/api/v1/integration-users?page%5Bnumber%5D=2&page%5Bsize%5D=2",
                            "last": "https://example.com/api/v1/integration-users?page%5Bnumber%5D=20371&page%5Bsize%5D=2"
                        }
                    }
                }
            }
        }
    }
)
async def list_integration_users(
    request: Request,
    page_size: int = Query(100, alias="page[size]", ge=1, le=1000, description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", ge=1, description="Page number (1-based)"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Returns all integration users in JSON API format with page-based pagination'''
    
    # Get paginated data
    result = repo.get_all_paginated("integrationUsers", page_number=page_number, page_size=page_size)
    
    # Convert to JSON API format
    integration_user_data = []
    for integration_user in result["items"]:
        integration_user_attributes = IntegrationUserAttributes(
            identifier=integration_user["identifier"],
            roles=integration_user["roles"],
            first_name=integration_user["first_name"],
            last_name=integration_user["last_name"],
            email=integration_user["email"],
            lti_consumer_user_id=integration_user["lti_consumer_user_id"],
            lti_lis_person_sourcedid=integration_user["lti_lis_person_sourcedid"],
            created_at=integration_user.get("created_at", ""),
            updated_at=integration_user.get("updated_at", "")
        )
        integration_user_item = IntegrationUserData(
            id=str(integration_user["id"]),
            attributes=integration_user_attributes
        )
        integration_user_data.append(integration_user_item)
    
    # Build pagination links
    links = build_pagination_links(request, result["page_number"], result["page_size"], result["total_pages"])
    
    return IntegrationUserListJsonApiResponse(data=integration_user_data, links=links.dict(exclude_none=True))

@integration_user_router.get(
    "/integration-users/{id}", 
    response_model=IntegrationUserJsonApiResponse,
    summary="Find Integration User by ID",
    responses={
        200: {
            "description": "Integration user details",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "2",
                            "type": "integration-users",
                            "attributes": {
                                "identifier": "rdegracia",
                                "roles": "Instructor",
                                "first-name": "Ria",
                                "last-name": "de Gracia",
                                "email": "r.degracia@federation.edu.au",
                                "lti-consumer-user-id": "130253",
                                "lti-lis-person-sourcedid": "rdegracia",
                                "created-at": "2018-12-20T04:16:51.000Z",
                                "updated-at": "2025-02-11T04:24:54.000Z"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Integration user not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Item with ID 2 not found in integration_users"
                        }]
                    }
                }
            }
        }
    }
)
async def get_integration_user(
    id: str = Path(..., description="Integration User ID"),
    repo: EReserveRepository = Depends(get_ereserve_repository)
):
    '''Get a specific integration user by ID in JSON API format'''
    integration_user = repo.get_by_id("integrationUsers", id)
    
    # Convert to JSON API format
    integration_user_attributes = IntegrationUserAttributes(
        identifier=integration_user["identifier"],
        roles=integration_user["roles"],
        first_name=integration_user["first_name"],
        last_name=integration_user["last_name"],
        email=integration_user["email"],
        lti_consumer_user_id=integration_user["lti_consumer_user_id"],
        lti_lis_person_sourcedid=integration_user["lti_lis_person_sourcedid"],
        created_at=integration_user.get("created_at", ""),
        updated_at=integration_user.get("updated_at", "")
    )
    integration_user_data = IntegrationUserData(
        id=str(integration_user["id"]),
        attributes=integration_user_attributes
    )
    
    return IntegrationUserJsonApiResponse(data=integration_user_data)

router = integration_user_router