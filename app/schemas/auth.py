from pydantic import BaseModel, field_validator
from datetime import datetime, timezone


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str   # JWT "sub" should be a string
    role: str
    exp: datetime

    @field_validator("exp", mode="before")
    @classmethod
    def convert_exp(cls, v):
        # Convert UNIX timestamp (int) -> datetime
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v

class RefreshTokenPayload(BaseModel):
    sub: str   # JWT "sub" should be a string
    exp: datetime

    @field_validator("exp", mode="before")
    @classmethod
    def convert_exp(cls, v):
        # Convert UNIX timestamp (int) -> datetime
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        return v
