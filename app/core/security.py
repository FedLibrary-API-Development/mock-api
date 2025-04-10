from fastapi import Security, HTTPException, Depends, status
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.core import settings
from app.core import logger

# Define the API key header
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validate the API key from the request header.
    """
    if api_key_header not in settings.API_KEYS:
        logger.warning(f"Invalid API key attempt: {api_key_header[:5]}..." if api_key_header else "No API key provided")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, 
            detail="Invalid or missing API key"
        )
    
    logger.debug(f"API request successfully authenticated with key.")
    return api_key_header