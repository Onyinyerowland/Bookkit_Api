from ..repositories.review_repo import ReviewRepo
from ..repositories.booking_repo import BookingRepo
from ..models import Review
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.repo = ReviewRepo(db)
        self.booking_repo = BookingRepo(db)


    async def create(self, booking_id, rating, comment, user_id):
        booking = await self.booking_repo.get(booking_id)
        if not booking:
            raise ValueError('booking_not_found')
        if booking.user_id != user_id:
            raise ValueError('forbidden')
        if booking.status != 'completed' and booking.status != 'completed':
            # ensure booking completed
            raise ValueError('booking_not_completed')
        existing = await self.repo.get_by_booking(booking_id)
        if existing:
            raise ValueError('already_reviewed')
        review = Review(booking_id=booking_id, rating=rating, comment=comment)
        return await self.repo.create(review)


    async def list_for_service(self, service_id):
        return await self.repo.list_for_service(service_id)


    async def get(self, id):
        return await self.repo.get(id)


    async def update(self, review, **data):
        return await self.repo.update(review, **data)


    async def delete(self, review):
        return await self.repo.delete(review)

    async def list(self, skip: int = 0, limit: int = 100):
        return await self.repo.list(skip=skip, limit=limit)

    async def count(self):
        return await self.repo.count()
