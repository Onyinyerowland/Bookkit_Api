from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime


class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    duration_minutes: int
    is_active: Optional[bool] = True


class ServiceCreate(ServiceBase):
    model_config = ConfigDict(from_attributes=True)


class ServiceOut(ServiceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
    @field_validator("price")
    @classmethod
    def check_price(cls, v: float) -> float:
        if v is not None and v < 0:
            raise ValueError("price must be non-negative")
        return v
    @field_validator("duration_minutes")
    @classmethod
    def check_duration(cls, v: int) -> int:
        if v is not None and v <= 0:
            raise ValueError("duration_minutes must be positive")
        return v
    @field_validator("title")
    @classmethod
    def check_title(cls, v: str) -> str:
        if v is not None and len(v) == 0:
            raise ValueError("title must be non-empty")
        return v

    @field_validator("description")
    @classmethod
    def check_description(cls, v: str) -> str:
        if v is not None and len(v) == 0:
            raise ValueError("description must be non-empty if provided")
        return v
    @field_validator("is_active")
    @classmethod
    def check_is_active(cls, v: bool) -> bool:
        if v is not None and not isinstance(v, bool):
            raise ValueError("is_active must be a boolean")
        return v
