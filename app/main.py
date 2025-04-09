import uvicorn
import time
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core import settings
from app.core import logger
from app.api.routes import resources
from app.utils import check_csv_file_exists
from app.api.errors import validation_exception_handler
from app.db import ResourceRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Add startup logic here
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    check_csv_file_exists(
        settings.CSV_FILE_FULL_PATH, 
        ResourceRepository.COLUMNS
    )
    logger.info(f"CSV file path: {settings.CSV_FILE_FULL_PATH}")
    yield
    
    # Add shutdown logic here (optional)
    logger.info(f"{settings.APP_NAME} shutdown complete")
    

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    
    Returns:
        Configured FastAPI application
    """
    
    # Create the FastAPI app
    app = FastAPI(
        lifespan=lifespan,
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],     # Set exact origins in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # Register routers
    app.include_router(resources.router, prefix="/api/v1/resources", tags=["resources"])
    
    # Add middleware for request logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.perf_counter()
        logger.debug(f"➡️ {request.method} {request.url.path}")
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        logger.debug(f"⬅️ {request.method} {request.url.path} completed in {process_time:.4f}s with status {response.status_code}")
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )