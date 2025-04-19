from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    disabled: bool = False