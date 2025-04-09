import pandas as pd
from typing import Optional, Dict, Any
from fastapi import HTTPException

from app.core import settings
from app.core import logger
from app.utils import read_csv_file, write_csv_file

class ResourceRepository:
    """Repository for CRUD operations on resources in a CSV file"""
    
    # Define columns for the CSV file
    COLUMNS = ["id", "title", "description", "access_count", "student_count"]
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the repository
        
        Args:
            file_path: Optional path to the CSV file. Path from settings will be used if not provided 
        """
        self.file_path = file_path or settings.CSV_FILE_FULL_PATH
        logger.debug(f"Initialized ResourceRepository with file path: {self.file_path}")
        
    
    def get_all(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Get all resources with pagination
        
        Args:
            skip: Number of resources to skip
            limit: Max no. of resources to return
            
        Returns:
            Dictionary with resources and count
        """
        df = read_csv_file(self.file_path, self.COLUMNS)
        total_count = len(df)
        
        # Apply pagination
        if not df.empty:
            df = df.iloc[skip:skip + limit]
            
        resources = df.to_dict("records")
        return {"resources": resources, "count": total_count}


    def get_by_id(self, resource_id: str) -> Dict[str, Any]:
        """
        Get a resource by ID.
        
        Args:
            resource_id: ID of the resource to get
            
        Returns:
            Dictionary of the resource
            
        Raises:
            HTTPException: If the resource is not found
        """
        df = read_csv_file(self.file_path, self.COLUMNS)
        resource = df[df["id"] == resource_id]
        
        if resource.empty:
            logger.warning(f"Resource not found: {resource_id}")
            raise HTTPException(status_code=404, detail=f"Resource with ID {resource_id} not found")
        
        return resource.to_dict("records")[0]
    
    
    def create(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new resource
        
        Args:
            resource_data: Data for the new resource
        
        Returns:
            Dictionary of the created resource
        """
        df = read_csv_file(self.file_path, self.COLUMNS)
        
        # Check if ID already exists
        if not df.empty and resource_data["id"] in df["id"].values:
            logger.warning(f"Resource with ID {resource_data['id']} already exists")
            raise HTTPException(status_code=400, detail=f"Resource with ID {resource_data['id']} already exists")
        
        # Append to DataFrame and save
        df = pd.concat([df, pd.DataFrame([resource_data])], ignore_index=True)
        write_csv_file(self.file_path, df)
        
        logger.info(f"Created resource with ID: {resource_data['id']}")

        return resource_data
        
        
    def update(self, resource_id: str, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing resource
        
        Args:
            resource_id: ID of the resource to update
            resource_data: New data for the resource
            
        Returns:
            Dictionary of the updated resource
            
        Raises:
            HTTPException: If the resource is not found
        """
        df = read_csv_file(self.file_path, self.COLUMNS)
        
        # Check if resource exists
        if not df.empty and not (df["id"] == resource_id).any():
            logger.warning(f"Resource not found: {resource_id}")
            raise HTTPException(status_code=404, detail=f"Resource with ID {resource_id} not found")
        
        # Update resource fields (only the provided fields)
        for key, value in resource_data.items():
            if key != "id" and value is not None:   # Don't update id and skip None values
                df.loc[df["id"] == resource_id, key] = value
        
        write_csv_file(self.file_path, df)
        
        # Return updated resource
        updated_resource = df[df["id"] == resource_id].to_dict("records")[0]
        logger.info(f"Updated resource with ID: {resource_id}")
        return updated_resource
    
    
    def delete(self, resource_id: str) -> Dict[str, str]:
        """
        Delete a resource
        
        Args:
            resource_id: ID of the resource to delete
            
        Returns:
            Dictionary with success message
            
        Raises:
            HTTPException: if the resource is not found
        """
        df = read_csv_file(self.file_path, self.COLUMNS)
        
        # Check if resource exists
        if not df.empty and not (df["id"] == resource_id).any():
            logger.warning(f"Resource not found: {resource_id}")
            raise HTTPException(status_code=404, detail=f"Resource with ID {resource_id} not found")
        
        # Remove resource
        df = df[df["id"] != resource_id]
        write_csv_file(self.file_path, df)
        
        logger.info(f"Deleted resource with ID: {resource_id}")
        return {"message": f"Resource with ID {resource_id} deleted successfully"}