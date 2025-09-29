from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, role: str, expires_delta: timedelta | None = None) -> str:
    expires = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MIN)
    )
    payload = {"sub": subject, "role": role, "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(subject: str, expires_days: int | None = None) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        days=expires_days or settings.REFRESH_TOKEN_EXPIRES_DAYS
    )
    payload = {"sub": subject, "type": "refresh", "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None


def refresh_access_token(refresh_token: str) -> str | None:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            return None
        subject = payload.get("sub")
        if subject is None:
            return None
        new_payload = {
            "sub": subject,
            "role": payload.get("role"),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MIN),
        }
        return jwt.encode(new_payload, settings.SECRET_KEY, algorithm="HS256")
    except JWTError:
        return None


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

