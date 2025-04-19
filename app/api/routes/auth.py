from datetime import timedelta
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import timedelta

from app.core import settings
from app.core.auth import create_access_token
from app.db import EReserveRepository

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str  # Not validated in mock version

@router.post("/users/login")
async def create_authenticated_session(login_data: LoginRequest, response: Response):
    """
    **Create new authenticated session**\n
    This method creates a new session for access to the API\n\n
    After calling this method a bearer will be generated in the header of the response which is then used when calling methods that require authentication. This bearer is time limited and will expire in 1:00 hour.
    """
    repo = EReserveRepository()
    try:
        # Check if user exists in mock data
        users = repo.get_all("users")["items"]
        integration_users = repo.get_all("integrationUsers")["items"]
        all_users = users + integration_users
        
        user = next((u for u in all_users if u.get("email") == login_data.email), None)
        
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        
        user_attributes = {
            "first_name": user.get("first_name"), 
            "last_name": user.get("last_name"), 
            "email": user.get("email"), 
            "created_at": user.get("created_at"), 
            "updated_at": user.get("updated_at")
        }
        
        # Password must be verified here.
        # Generating a token since this is a mock API
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": login_data.email}, 
            expires_delta=access_token_expires
        )
        
        # Set the token in the header instead of returning it in the body
        response.headers["Authorization"] = f"Bearer {access_token}"
        
        # Return a 204 No Content or a simple success message
        return {"id": user.get("id"), "attributes": user_attributes}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    