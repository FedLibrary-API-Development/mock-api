import json
from typing import Optional, Dict, Any
from fastapi import HTTPException

from app.core import settings
from app.core import logger

class EReserveRepository:
    """Repository for CRUD operations on sample data in JSON file"""
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the repository
        
        Args:
            file_path: Optional path to the JSON file. Path from settings will be used if not provided 
        """
        self.file_path = file_path or settings.JSON_FILE_FULL_PATH
        logger.debug(f"Initialized EReserveRepository with file path: {self.file_path}")
        self._data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"JSON file not found at {self.file_path}")
            raise HTTPException(status_code=500, detail="Data file not found")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file at {self.file_path}")
            raise HTTPException(status_code=500, detail="Invalid data file format")

    def get_all(self, collection: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Get all items from a collection with pagination
        
        Args:
            collection: Name of the collection to query
            skip: Number of items to skip
            limit: Max no. of items to return
            
        Returns:
            Dictionary with items and count
        """
        if collection not in self._data:
            raise HTTPException(status_code=404, detail=f"Collection {collection} not found")
            
        items = self._data[collection]
        total_count = len(items)
        
        # Apply pagination
        items = items[skip:skip + limit]
        return {"items": items, "count": total_count}

    def get_by_id(self, collection: str, item_id: int) -> Dict[str, Any]:
        """
        Get an item by ID from a collection.
        
        Args:
            collection: Name of the collection to query
            item_id: ID of the item to get
            
        Returns:
            Dictionary of the item
            
        Raises:
            HTTPException: If the item is not found
        """
        if collection not in self._data:
            raise HTTPException(status_code=404, detail=f"Collection {collection} not found")
            
        for item in self._data[collection]:
            if item.get("id") == item_id:
                return item
        
        logger.warning(f"Item not found in {collection}: {item_id}")
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found in {collection}")