from ..repositories.service_repo import ServiceRepo
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceService:
    def __init__(self, db: AsyncSession):
        self.repo = ServiceRepo(db)


    async def list(self, q=None, price_min=None, price_max=None, active=None):
        return await self.repo.list(q, price_min, price_max, active)


    async def create(self, data):
        return await self.repo.create(**data)


    async def get(self, id):
        return await self.repo.get(id)


    async def update(self, svc, data):
        return await self.repo.update(svc, **data)


    async def delete(self, svc):
        return await self.repo.delete(svc)

    async def count(self):
        return await self.repo.count()
    async def list_all(self, skip: int = 0, limit: int = 100):
        return await self.repo.list_all(skip=skip, limit=limit)
    
