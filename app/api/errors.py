from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core import logger


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for validation errors
    
    Args:
        request: Request that caused the exception
        exc: Exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
        
    logger.warning(f"Validation error: {error_details}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": error_details,
            "message": "Validation error"
        },
    )