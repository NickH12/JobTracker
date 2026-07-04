# post /auth/login schema that accept UserLogin and return a token, raise 401 if invalid credentials
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

