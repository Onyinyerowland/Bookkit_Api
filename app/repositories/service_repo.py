from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ..models import Service
from typing import List, Optional


class ServiceRepo:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def list(self, q: Optional[str]=None, price_min: Optional[float]=None, price_max: Optional[float]=None, active: Optional[bool]=None):
        stmt = select(Service)
        filters = []
        if q:
            filters.append(Service.title.ilike(f"%{q}%"))
        if price_min is not None:
            filters.append(Service.price >= price_min)
        if price_max is not None:
            filters.append(Service.price <= price_max)
        if active is not None:
            filters.append(Service.is_active == active)
        if filters:
            stmt = stmt.where(and_(*filters))
        r = await self.db.execute(stmt)
        return r.scalars().all()


    async def get(self, id):
        r = await self.db.execute(select(Service).where(Service.id == id))
        return r.scalars().first()


    async def create(self, **data):
        s = Service(**data)
        self.db.add(s)
        await self.db.commit()
        await self.db.refresh(s)
        return s


    async def update(self, service: Service, **data):
        for k,v in data.items(): setattr(service, k, v)
        self.db.add(service)
        await self.db.commit()
        await self.db.refresh(service)
        return service


    async def delete(self, service: Service):
        await self.db.delete(service)
        await self.db.commit()
        return service
    async def count(self):
        q = select(Service)
        r = await self.db.execute(q)
        return r.scalars().count()

