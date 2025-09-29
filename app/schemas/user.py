from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str

    model_config = ConfigDict(from_attributes=True)
class UserCount(BaseModel):
    count: int

    model_config = ConfigDict(from_attributes=True)
class UserList(BaseModel):
    users: list[UserOut]

    model_config = ConfigDict(from_attributes=True)
class UserPagination(BaseModel):
    total: int
    page: int
    size: int
    users: list[UserOut]

    model_config = ConfigDict(from_attributes=True)
class UserDeleteResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    message: str

    model_config = ConfigDict(from_attributes=True)

