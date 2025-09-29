from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review
from sqlalchemy import select

class ReviewRepo:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, review: Review):
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_by_booking(db: AsyncSession, booking_id: int):
        res = await db.execute(select(Review).where(Review.booking_id == booking_id))
        return res.scalars().first()

    async def get_by_id(db: AsyncSession, review_id: int):
        res = await db.execute(select(Review).where(Review.id == review_id))
        return res.scalars().first()
    async def delete(self, review: Review):
        await self.db.delete(review)
        await self.db.commit()
        return review
    async def update(self, review: Review, **data):
        for k,v in data.items():
            setattr(review, k, v)
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review
    async def list(self, skip: int = 0, limit: int = 100):
        q = select(Review).offset(skip).limit(limit)
        r = await self.db.execute(q)
        return r.scalars().all()
    async def count(self):
        q = select(Review)
        r = await self.db.execute(q)
        return r.scalars().count()

