from fastapi import APIRouter, Depends, HTTPException
from ..deps import get_current_user
from  app.schemas.user import UserOut, UserUpdate
from ..services.auth_service import AuthService
from ..deps import get_db_session
from ..repositories.user_repo import UserRepo


router = APIRouter()

# Removed the incorrect assignment

@router.get('/', response_model=UserOut)
async def me(user = Depends(get_current_user)):
    return user



@router.patch('/')
async def update_me(payload: UserUpdate, user = Depends(get_current_user), db = Depends(get_db_session)):
    svc = AuthService(db)
        # only implement change of name/email/password
    fields = {}
    if payload.name: fields['name'] = payload.name
    if payload.email: fields['email'] = payload.email
    if payload.password:
        fields['password_hash'] = svc.user_repo.hash_password(payload.password)

        # For brevity: call repository directly
    repo = UserRepo(db)
    updated = await repo.update(user, **{k:v for k,v in fields.items() if v is not None})
    return {'id': str(updated.id), 'email': updated.email, 'name': updated.name}


    # return updated
    # try:
    #     updated = await svc.update_user(user.id, **fields)

    #     return {'id': str(updated.id), 'email': updated.email, 'name': updated.name}
    # except ValueError as e:
    #     if str(e) == 'email_exists':
    #         raise HTTPException(409, 'Email already registered')
