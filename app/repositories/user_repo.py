from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import User
from ..schemas.user import UserCreate
from typing import Optional, List


class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_email(self, email: str) -> Optional[User]:
        q = select(User).where(User.email == email)
        r = await self.db.execute(q)
        return r.scalars().first()


    async def get(self, user_id):
        q = select(User).where(User.id == user_id)
        r = await self.db.execute(q)
        return r.scalars().first()


    async def create(self, name: str, email: str, password_hash: str):
        user = User(name=name, email=email, password_hash=password_hash)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


    async def update(self, user: User, **fields):
        for k,v in fields.items():
            setattr(user, k, v)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.commit()
        return user

    async def list(self, skip: int = 0, limit: int = 100):
        q = select(User).offset(skip).limit(limit)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def count(self):
        q = select(User)
        r = await self.db.execute(q)
        return r.scalars().count()

    async def get_by_name(self, name: str) -> Optional[User]:
        q = select(User).where(User.name == name)
        r = await self.db.execute(q)
        return r.scalars().first()

    async def get_by_role(self, role: str) -> Optional[User]:
        q = select(User).where(User.role == role)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_all(self) -> List[User]:
        q = select(User)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_by_ids(self, user_ids: List[int]) -> List[User]:
        q = select(User).where(User.id.in_(user_ids))
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_by_emails(self, emails: List[str]) -> List[User]:
        q = select(User).where(User.email.in_(emails))
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_by_names(self, names: List[str]) -> List[User]:
        q = select(User).where(User.name.in_(names))
        r = await self.db.execute(q)
        return r.scalars().all()
    async def get_active_users(self) -> List[User]:
        q = select(User).where(User.is_active == True)
        r = await self.db.execute(q)
        return r.scalars().all()
    async def get_inactive_users(self) -> List[User]:
        q = select(User).where(User.is_active == False)
        r = await self.db.execute(q)
        return r.scalars().all()
    async def activate_user(self, user: User):
        user.is_active = True
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    async def deactivate_user(self, user: User):
        user.is_active = False
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
