from datetime import timedelta
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr
from datetime import timedelta

from app.core import settings
from app.core.auth import create_access_token
from app.db import EReserveRepository

router = APIRouter()

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    public_v1_user: UserCredentials

class UserAttributes(BaseModel):
    first_name: str
    last_name: str
    email: str
    created_at: str
    updated_at: str

class UserData(BaseModel):
    id: str
    type: str = "users"
    attributes: UserAttributes

class LoginResponse(BaseModel):
    data: UserData

@router.post(
    "/users/login",
    response_model=LoginResponse,
    responses={
        200: {
            "description": "Successful authentication",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "data": {
                            "id": "123",
                            "type": "users",
                            "attributes": {
                                "first_name": "John",
                                "last_name": "Doe",
                                "email": "user@example.edu",
                                "created_at": "2025-01-01T00:00:00Z",
                                "updated_at": "2025-01-01T00:00:00Z"
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid credentials or user not found",
            "content": {
                "application/vnd.api+json": {
                    "example": {
                        "errors": [{
                            "status": "400",
                            "title": "Authentication Error",
                            "detail": "Incorrect email or password"
                        }]
                    }
                }
            }
        }
    }
)
async def create_authenticated_session(login_data: LoginRequest, response: Response):
    """
    **Create new authenticated session**\n
    This method creates a new session for access to the API\n\n
    After calling this method a bearer will be generated in the header of the response which is then used when calling methods that require authentication. This bearer is time limited and will expire in 1:00 hour.
    """
    repo = EReserveRepository()
    try:
        # Extract user credentials from the nested structure
        user_credentials = login_data.public_v1_user
        # Check if user exists in mock data
        users = repo.get_all("users")["items"]
        integration_users = repo.get_all("integrationUsers")["items"]
        all_users = users + integration_users
        
        user = next((u for u in all_users if u.get("email") == user_credentials.email), None)
        
        if not user:
            raise HTTPException(
                status_code=400, 
                detail={
                    "errors": [{
                        "status": "400",
                        "title": "Authentication Error",
                        "detail": "Incorrect email or password"
                    }]
                }
            )
        
        # Password must be verified here.
        # Generating a token since this is a mock API
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_credentials.email}, 
            expires_delta=access_token_expires
        )
        
        # Set the token in the header
        response.headers["Authorization"] = f"Bearer {access_token}"
        
        # Set content type for JSON API
        response.headers["Content-Type"] = "application/vnd.api+json"    
        
        user_attributes = {
            "first_name": user.get("first_name", ""), 
            "last_name": user.get("last_name", ""), 
            "email": user.get("email", ""), 
            "created_at": user.get("created_at", ""), 
            "updated_at": user.get("updated_at", "")
        }
        
        user_data = UserData(
            id=str(user.get("id", "")),
            attributes=user_attributes
        )
        
        return LoginResponse(data=user_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail={
                "errors": [{
                    "status": "400",
                    "title": "Server Error",
                    "detail": str(e)
                }]
            }
        )
    