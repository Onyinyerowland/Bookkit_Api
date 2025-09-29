from ..repositories.user_repo import UserRepo
from ..utils import hash_password, verify_password, create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepo(db)


    async def register(self, name, email, password):
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError('email_exists')
        pw_hash = hash_password(password)
        user = await self.user_repo.create(name, email, pw_hash)
        return user


    async def login(self, email, password):
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError('invalid')
        if not verify_password(password, user.password_hash):
            raise ValueError('invalid')
        access = create_access_token(str(user.id), user.role.value)
        refresh = create_refresh_token(str(user.id), user.role.value)
        return user, access, refresh

    async def get_user(self, user_id):
        user = await self.user_repo.get(user_id)
        if not user:
            raise ValueError('not_found')
        return user

    async def refresh_tokens(self, user_id):
        user = await self.user_repo.get(user_id)
        if not user:
            raise ValueError('not_found')
        access = create_access_token(str(user.id), user.role.value)
        refresh = create_refresh_token(str(user.id), user.role.value)
        return access, refresh

    async def change_password(self, user_id, old_password, new_password):
        user = await self.user_repo.get(user_id)
        if not user:
            raise ValueError('not_found')
        if not verify_password(old_password, user.password_hash):
            raise ValueError('invalid')
        new_hash = hash_password(new_password)
        user = await self.user_repo.update(user, password_hash=new_hash)
        return user

    async def reset_password(self, email, new_password):
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError('not_found')
        new_hash = hash_password(new_password)
        user = await self.user_repo.update(user, password_hash=new_hash)
        return user

