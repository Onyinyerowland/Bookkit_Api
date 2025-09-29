from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    booking_id: int
    rating: int
    comment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewOut(BaseModel):
    id: int
    booking_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    @field_validator("rating")
    @classmethod
    def check_rating(cls, v: int) -> int:
        if v and (v < 1 or v > 5):
            raise ValueError("rating must be between 1 and 5")
        return v
    @field_validator("comment")
    @classmethod
    def check_comment(cls, v: str) -> str:
        if v and len(v) > 500:
            raise ValueError("comment must be at most 500 characters")
        return v
    @field_validator("booking_id", check_fields=False)
    @classmethod
    def check_booking_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("booking_id must be a positive integer")
        return v
