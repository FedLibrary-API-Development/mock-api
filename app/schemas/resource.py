import uuid
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class ResourceBase(BaseModel):
    """Base Pydantic model for resources"""
    title: str = Field(..., description="Title of the resource", example="Software Architecture Docs")
    description: Optional[str] = Field(None, description="Description of the resource", example="System design patterns and documentation")
    access_count: int = Field(..., description="Access count of the resource", example="5432")
    student_count: int = Field(..., description="No. of students who accessed the resource", example="275")
    

class ResourceCreate(ResourceBase):
    """Pydantic model for creating a resource"""
    id: Optional[str] = Field(None, description="Optional resource ID (auto generated if not provided)")
    
    @field_validator("id", mode="before")
    @classmethod
    def set_id(cls, v):
        """Generate a UUID if id is not provided."""
        return v or str(uuid.uuid4())


class ResourceUpdate(ResourceBase):
    """Pydantic model for updating a resource"""
    title: Optional[str] = Field(None, description="Title of the resource")
    description: Optional[str] = Field(None, description="Description of the resource")
    access_count: Optional[int] = Field(None, description="Access count of the resource")
    student_count: Optional[int] = Field(None, description="No. of students who accessed the resource")
    
    
class ResourceInDB(ResourceBase):
    """Pydantic model for a resource in the database"""
    id: str = Field(..., description="Unique identifier for the resource")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Software Architecture Docs",
                "description": "System design patterns and documentation",
                "access_count": 642,
                "student_count": 48
            }
        }   
        
        
class ResourceResponse(ResourceInDB):
    """Pydantic model for an resource response"""
    pass


class ResourceListResponse(BaseModel):
    """Pydantic model for a list of resources response"""
    resources: List[ResourceResponse]
    count: int 