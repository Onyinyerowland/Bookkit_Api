from ..repositories.booking_repo import BookingRepo
from ..repositories.service_repo import ServiceRepo
from ..models import Booking
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta


class BookingService:
    def __init__(self, db: AsyncSession):
        self.repo = BookingRepo(db)
        self.service_repo = ServiceRepo(db)


    async def create(self, user_id, service_id, start_time):
        service = await self.service_repo.get(service_id)
        if not service:
            raise ValueError('service_not_found')
        end_time = start_time + timedelta(minutes=service.duration_minutes)
            # check overlap
        overlaps = await self.repo.overlaps(service_id, start_time, end_time)
        if overlaps:
            raise ValueError('slot_conflict')
        booking = Booking(user_id=user_id, service_id=service_id, start_time=start_time, end_time=end_time)
        return await self.repo.create(booking)


    async def list_for_user(self, user_id):
        return await self.repo.list_for_user(user_id)


    async def list_all(self, status=None, from_dt=None, to_dt=None):
        return await self.repo.list_all(status, from_dt, to_dt)


    async def get(self, id):
        return await self.repo.get(id)


    async def update(self, booking, **data):
        return await self.repo.update(booking, **data)


    async def delete(self, booking):
        return await self.repo.delete(booking)
