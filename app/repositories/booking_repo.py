from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from sqlalchemy import and_, or_
from app.models.booking import Booking
class BookingRepo:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, booking: Booking):
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking


    async def get(self, id):
        r = await self.db.execute(select(Booking).where(Booking.id == id))
        return r.scalars().first()


    async def list_for_user(self, user_id):
        r = await self.db.execute(select(Booking).where(Booking.user_id == user_id))
        return r.scalars().all()


    async def list_all(self, status=None, from_dt=None, to_dt=None):
        stmt = select(Booking)
        filters = []
        if status:
            filters.append(Booking.status == status)
        if from_dt:
            filters.append(Booking.start_time >= from_dt)
        if to_dt:
            filters.append(Booking.start_time <= to_dt)
        if filters:
            stmt = stmt.where(and_(*filters))
        r = await self.db.execute(stmt)
        return r.scalars().all()


    async def overlaps(self, service_id, start_time, end_time):
        # Checks for bookings that overlap the requested slot for the same service
        stmt = select(Booking).where(
            Booking.service_id == service_id,
            or_(
                and_(Booking.start_time <= start_time, Booking.end_time > start_time),
                and_(Booking.start_time < end_time, Booking.end_time >= end_time),
                and_(Booking.start_time >= start_time, Booking.end_time <= end_time)
            ),
            Booking.status != 'cancelled'
       )
        r = await self.db.execute(stmt)
        return r.scalars().first() is not None


    async def delete(self, booking: Booking):
        await self.db.delete(booking)
        await self.db.commit()


    async def update(self, booking: Booking, **data):
        for k,v in data.items(): setattr(booking, k, v)
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking
    
    async def count(self):
        r = await self.db.execute(select(func.count(Booking.id)))
        return r.scalar_one()
