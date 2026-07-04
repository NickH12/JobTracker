#make a schema user from pydantic import BaseModel, EmailStr
# No — don't import SQLAlchemy Declarative Base here.
# Schemas should use pydantic.BaseModel
# enable from_atributes = True


from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    # from_attributes v2 style
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime