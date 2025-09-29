from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime, timezone
from typing import Optional


class BookingCreate(BaseModel):
    service_id: int
    start_time: datetime
    end_time : datetime

    @field_validator("start_time")
    def check_start_time(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("start_time must be in the future")
        return v

    model_config = ConfigDict(from_attributes=True)


class BookingOut(BaseModel):
    id: int
    user_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    @field_validator("start_time")
    def check_start_time(cls, v: datetime) -> datetime:
        if v and v < datetime.now(timezone.utc):
            raise ValueError("start_time must be in the future")
        return v
    @field_validator("status")
    def check_status(cls, v: str) -> str:
        allowed = {'pending', 'confirmed', 'completed', 'cancelled'}
        if v and v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v
    
