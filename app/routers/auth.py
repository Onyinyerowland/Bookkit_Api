from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db_session, get_current_user
from app.schemas.auth import Token
from app.schemas.user import UserOut, UserCreate, UserLogin, ChangePasswordRequest, ResetPasswordRequest
from app.services.auth_service import AuthService
from app.models.user import User
from app.utils.security import create_access_token, decode_token
from typing import Optional

router = APIRouter()

# ---------- Register ----------
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db_session)):
    svc = AuthService(db)
    try:
        user = await svc.register(payload.name, payload.email, payload.password)
        return user
    except ValueError as e:
        if str(e) == "email_exists":
            raise HTTPException(status_code=409, detail="Email already registered")
        raise


# ---------- Login ----------
@router.post("/login", response_model=Token)
async def login(response: Response, payload: UserLogin, db: AsyncSession = Depends(get_db_session)):
    svc = AuthService(db)
    try:
        user, access, refresh = await svc.login(payload.email, payload.password)
        response.set_cookie("refresh_token", refresh, httponly=True, path="/auth/refresh")
        return {"access_token": access, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# ---------- Refresh ----------
@router.post("/refresh", response_model=Token)
async def refresh(response: Response, refresh_token: str = Cookie(None), db: AsyncSession = Depends(get_db_session)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access = create_access_token(payload["sub"], payload.get("role", "user"))
    return {"access_token": access, "token_type": "bearer"}


# ---------- Logout ----------
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie("refresh_token", path="/auth/refresh")
    return Response(status_code=204)


# ---------- Change Password ----------
@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    payload: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    svc = AuthService(db)
    try:
        await svc.change_password(current_user.id, payload.old_password, payload.new_password)
        return Response(status_code=204)
    except ValueError as e:
        if str(e) == "invalid":
            raise HTTPException(status_code=401, detail="Invalid current password")
        raise


# ---------- Reset Password ----------
@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db_session)):
    svc = AuthService(db)
    try:
        await svc.reset_password(payload.email, payload.new_password)
        return Response(status_code=204)
    except ValueError as e:
        if str(e) == "not_found":
            raise HTTPException(status_code=404, detail="User not found")
        raise
# ---------- Get Current User ----------
@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
