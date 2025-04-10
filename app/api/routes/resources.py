from fastapi import APIRouter, Query, Depends, Path

from app.db import ResourceRepository
from app.api.dependencies import get_resource_repository
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
    ResourceListResponse
)
from app.core import get_api_key


router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/", response_model=ResourceListResponse, summary="Get all resources")
async def get_resources(
    skip: int = Query(0, ge=0, description="Number of resources to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum no. of resources to return"),
    repository: ResourceRepository = Depends(get_resource_repository)
):
    """
    Get all resources with pagination
    
    - **skip**: No. of resources to skip
    - **limit** Max no. of resources to return
    """
    return repository.get_all(skip=skip, limit=limit)


@router.get("/{resource_id}", response_model=ResourceResponse, summary="Get a resource by ID")
async def get_resource(
    resource_id: str = Path(..., description="The ID of the resource to get"),
    repository: ResourceRepository = Depends(get_resource_repository)
):
    """
    Get a resource by its ID.
    
    - **resource_id**: The ID of the resource to get
    """
    return repository.get_by_id(resource_id=resource_id)


@router.post("/", response_model=ResourceResponse, status_code=201, summary="Create a new resource")
async def create_resource(
    resource: ResourceCreate,
    repository: ResourceRepository = Depends(get_resource_repository)
):
    """
    Create a new resource.
    
    - **id**: Optional. A unique identifier for the resource (will be generated if not provided)
    - **title**: Required. The title of the resource
    - **description**: Optional. A description of the resource
    - **access_count**: Required. Total access count
    - **student_count**: Required. Total no. of students
    """
    return repository.create(resource_data=resource.model_dump())


@router.put("/{resource_id}", response_model=ResourceResponse, summary="Update a resource")
async def update_resource(
    resource_id: str = Path(..., description="The ID of the resource to update"),
    resource: ResourceUpdate = ...,
    repository: ResourceRepository = Depends(get_resource_repository)
):
    """
    Update an existing resource.
    
    - **resource_id**: The ID of the resource to update
    - **title**: Optional. The new title of the resource
    - **description**: Optional. The new description of the resource
    - **access_count**: Optional. The new access count
    - **student_count**: Optional. The new student count
    """
    # Filter out None values
    update_data = {k: v for k, v in resource.model_dump().items() if v is not None}
    return repository.update(resource_id=resource_id, resource_data=update_data)


@router.delete("/{resource_id}", summary="Delete a resource")
async def delete_resource(
    resource_id: str = Path(..., description="The ID of the resource to delete"),
    repository: ResourceRepository = Depends(get_resource_repository)
):
    """
    Delete a resource.
    
    - **resource_id**: The ID of the resource to delete
    """
    return repository.delete(resource_id=resource_id)