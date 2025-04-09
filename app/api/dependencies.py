from app.db import ResourceRepository


def get_resource_repository() -> ResourceRepository:
    """
    Dependency for getting the resource repository
    
    Returns:
        An instance of ResourceRepository
    """
    return ResourceRepository()