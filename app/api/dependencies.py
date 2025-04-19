from fastapi import Depends

# from app.db import ResourceRepository
from app.db import EReserveRepository
from app.core import get_current_user


# def get_resource_repository() -> ResourceRepository:
#     """
#     Dependency for getting the resource repository
    
#     Returns:
#         An instance of ResourceRepository
#     """
#     return ResourceRepository()

def get_ereserve_repository() -> EReserveRepository:
    """Dependency for getting the eReserve repository"""
    return EReserveRepository()

def get_authenticated_user() -> dict:
    """Dependency for getting the current authenticated user"""
    return Depends(get_current_user)