from fastapi.openapi.utils import get_openapi

from app.core import settings

def custom_openapi(app):
    """
    Customize the OpenAPI schema for the application with security requirements.
    
    Args:
        app: The FastAPI application instance
        
    Returns:
        Dict[str, Any]: The customized OpenAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Mock API - Team B",
        version=settings.APP_VERSION,
        description="Mock API for simulating eReserve+ Analytics API",
        routes=app.routes,
    )
    
    # Add servers configuration to ensure proper URL construction
    openapi_schema["servers"] = [
        {"url": "/api/v1", "description": "Mock API v1"}
    ]

    
    # Store the original components that we need to preserve
    original_components = openapi_schema.get("components", {})
    original_schemas = original_components.get("schemas", {})
    
    # Create new components with preserved schemas
    components = {
        "schemas": original_schemas,
        "securitySchemes": {
            "HTTPBearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "This Mock API uses JSON Web Tokens (JWT) for authenticated access. Following are the steps to get the JWT bearer and how to use it:\n\n"
                "1.Login"
                "\n\nYou can login using the credentials of a user defined in the mock API sample dataset. You may use the email address \"admin@example.edu\". "
                "You may use any password since it is not validated by the mock API. Login can easily be done using /users/login in this documentation.\n\n"
                "On login the bearer will appear in the authorization header in the format:\n"
                "Bearer xxxxxx.yyyyyyy.zzzzzz\n\n"
                "2.Using the Bearer"
                "\n\nFor those API methods that require authentication you can include the bearer in the Authorization header. "
                "To have this happen automatically in this documentation simply place the bearer generated by your login "
                "(including the word \"Bearer\" onwards) in the field below.\n\n"
            }
        }
    }
    
    # Update the components instead of replacing them completely
    openapi_schema["components"] = components
    
    # Apply security globally
    openapi_schema["security"] = [{"HTTPBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema
