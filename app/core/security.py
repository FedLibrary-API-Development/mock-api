from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.core.auth import decode_token
from app.db import EReserveRepository

bearer_scheme = HTTPBearer(auto_error=False, scheme_name="HTTPBearer")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Validate the bearer token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Verify user exists
    repo = EReserveRepository()
    users = repo.get_all("users")["items"]
    integration_users = repo.get_all("integrationUsers")["items"]
    if not any(u.get("email") == username for u in users + integration_users):
        raise credentials_exception
    
    return {"username": username}