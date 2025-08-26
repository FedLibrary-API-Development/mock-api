import uvicorn
import time
import json
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html
from fastapi.responses import JSONResponse

from app.core import settings
from app.core import logger
from app.api.routes import auth
from app.api.routes.ereserve import ereserve_router
from app.api.errors import validation_exception_handler
from app.core.openapi import custom_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Add startup logic here
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

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
        version=settings.APP_VERSION
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
    
    # Global exception handler for JSON API format
    @app.exception_handler(HTTPException)
    async def json_api_exception_handler(request: Request, exc: HTTPException):
        # Define which endpoints should use JSON API format
        json_api_endpoints = settings.JSON_API_ENDPOINTS
        
        # Check if this is a JSON API endpoint
        is_json_api_endpoint = (
            any(request.url.path.endswith(endpoint) for endpoint in json_api_endpoints) or
            request.headers.get("accept") == "application/vnd.api+json" or
            request.headers.get("content-type") == "application/vnd.api+json"
        )
        
        if is_json_api_endpoint:
            # Format error in JSON API format
            if isinstance(exc.detail, dict) and "errors" in exc.detail:
                # Already in JSON API format
                return JSONResponse(
                    status_code=exc.status_code,
                    content=exc.detail,
                    headers={"Content-Type": "application/vnd.api+json"}
                )
            else:
                # Convert to JSON API format
                return JSONResponse(
                    status_code=exc.status_code,
                    content={
                        "errors": [{
                            "status": str(exc.status_code),
                            "title": "Error",
                            "detail": str(exc.detail)
                        }]
                    },
                    headers={"Content-Type": "application/vnd.api+json"}
                )
        
        # Default JSON response for other endpoints
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    # Register routers
    app.include_router(auth.router, tags=["User"])
    app.include_router(ereserve_router)
    
    # Add middleware for request logging
    @app.middleware("http")
    async def log_requests_and_json_api(request: Request, call_next):
        start_time = time.perf_counter()
        logger.debug(f"➡️ {request.method} {request.url.path}")
        
        # Define which endpoints should use JSON API format
        json_api_endpoints = settings.JSON_API_ENDPOINTS
        
        # JSON API middleware logic for specified endpoints
        is_json_api_endpoint = any(request.url.path.endswith(endpoint) for endpoint in json_api_endpoints)
        
        if (is_json_api_endpoint and 
            request.method in ["POST", "PUT", "PATCH"] and
            request.headers.get("content-type") == "application/vnd.api+json"):
            
            # Read the request body
            body = await request.body()
            if body:
                try:
                    # Parse JSON and validate structure
                    data = json.loads(body)
                    
                    # Validation logic can be endpoint-specific
                    if request.url.path.endswith("/users/login"):
                        if "public_v1_user" not in data:
                            return JSONResponse(
                                status_code=400,
                                content={
                                    "errors": [{
                                        "status": "400",
                                        "title": "Invalid Request Format",
                                        "detail": "Request must contain 'public_v1_user' object"
                                    }]
                                },
                                headers={"Content-Type": "application/vnd.api+json"}
                            )
                    
                except json.JSONDecodeError:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "errors": [{
                                "status": "400",
                                "title": "Invalid JSON",
                                "detail": "Request body must be valid JSON"
                            }]
                        },
                        headers={"Content-Type": "application/vnd.api+json"}
                    )
        
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        logger.debug(f"⬅️ {request.method} {request.url.path} completed in {process_time:.4f}s with status {response.status_code}")
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response
    
    return app

app = create_app()

# Apply custom OpenAPI
app.openapi = lambda: custom_openapi(app)

# Handle redirect for OAuth if needed
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# Create a root FastAPI app to mount the app at /api/v1
root_app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None,  # Disable docs at root level
    redoc_url=None,  # Disable redoc at root level
    openapi_url=None  # Disable OpenAPI schema at root level
)

# Mount the main app at /api/v1
root_app.mount("/api/v1", app)

# Redirect root to docs
@root_app.get("/", include_in_schema=False)
async def redirect_to_docs():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/v1/docs")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:root_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )