import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


def generate_uuid():
    return str(uuid.uuid4())


class ResourceBase(BaseModel):
    """Base Pydantic model for resources"""
    title: str = Field(..., description="Title of the resource", json_schema_extra={"example": "Software Architecture Docs"})
    description: Optional[str] = Field(None, description="Description of the resource", json_schema_extra={"example": "System design patterns and documentation"})
    access_count: int = Field(..., description="Access count of the resource", json_schema_extra={"example": 5432})
    student_count: int = Field(..., description="No. of students who accessed the resource", json_schema_extra={"example": 275})
    
    
class ResourceCreate(ResourceBase):
    """Pydantic model for creating a resource"""
    id: Optional[str] = Field(default_factory=generate_uuid, description="Optional resource ID (auto generated if not provided)")


class ResourceUpdate(ResourceBase):
    """Pydantic model for updating a resource"""
    title: Optional[str] = Field(None, description="Title of the resource")
    description: Optional[str] = Field(None, description="Description of the resource")
    access_count: Optional[int] = Field(None, description="Access count of the resource")
    student_count: Optional[int] = Field(None, description="No. of students who accessed the resource")
    
    
class ResourceInDB(ResourceBase):
    """Pydantic model for a resource in the database"""
    id: str = Field(..., description="Unique identifier for the resource")
    
    model_config = ConfigDict (
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Software Architecture Docs",
                "description": "System design patterns and documentation",
                "access_count": 642,
                "student_count": 48
            }
        }  
    )
        
        
class ResourceResponse(ResourceInDB):
    """Pydantic model for an resource response"""
    pass


class ResourceListResponse(BaseModel):
    """Pydantic model for a list of resources response"""
    resources: List[ResourceResponse]
    count: int 