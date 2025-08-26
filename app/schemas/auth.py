from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCredentials(BaseModel):
    """User credentials for login"""
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """JSON API formatted login request"""
    public_v1_user: UserCredentials

class UserAttributes(BaseModel):
    """User attributes in JSON API format"""
    first_name: str
    last_name: str
    email: str
    created_at: str
    updated_at: str
    
class UserData(BaseModel):
    """User data in JSON API format"""
    id: str
    type: str = "users"
    attributes: UserAttributes

class LoginResponse(BaseModel):
    """JSON API formatted login response"""
    data: UserData
    
class JsonApiError(BaseModel):
    """JSON API error format"""
    status: str
    title: str
    detail: str

class JsonApiErrorResponse(BaseModel):
    """JSON API error response format"""
    errors: list[JsonApiError]