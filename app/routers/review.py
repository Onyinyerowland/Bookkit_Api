from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.review import ReviewCreate, ReviewOut
from app.deps import get_current_user, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/reviews', tags=['reviews'])

@router.post(' ', response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_review(payload: ReviewCreate, db: AsyncSession = Depends(get_db_session), user=Depends(get_current_user)):
    # Validate booking completed and owned by user
    from app.repositories.booking_repo import BookingRepo
    repo_b = BookingRepo(db)
    booking = await repo_b.get_by_id(payload.booking_id)
    if not booking or booking.user_id != user.id or booking.status != 'completed':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Booking not eligible for review')
    # ensure one review per booking
    from app.repositories.review_repo import get_by_booking
    existing = await get_by_booking(db, payload.booking_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Review already exists')
    from app.models.review import Review
    r = Review(booking_id=payload.booking_id, rating=payload.rating, comment=payload.comment)
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r

@router.get('{service_id}', response_model=list[ReviewOut])
async def list_service_reviews(service_id: int, db: AsyncSession = Depends(get_db_session)):
    from sqlalchemy import select
    from app.models.review import Review
    from app.models.booking import Booking
    q = select(Review).join(Booking).where(Booking.service_id == service_id)
    res = await db.execute(q)
    return res.scalars().all()

@router.patch('{id}', response_model=ReviewOut)
async def patch_review(id: int, payload: ReviewCreate, db: AsyncSession = Depends(get_db_session), user=Depends(get_current_user)):
    from app.models.review import Review
    from sqlalchemy import select
    res = await db.execute(select(Review).where(Review.id == id))
    r = res.scalars().first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # check owner
    from app.repositories.booking_repo import BookingRepo
    booking = await BookingRepo(db).get_by_id(r.booking_id)
    if booking.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    r.rating = payload.rating
    r.comment = payload.comment
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r

@router.delete('{id}')
async def delete_review(id: int, db: AsyncSession = Depends(get_db_session), user=Depends(get_current_user)):
    from app.models.review import Review
    from sqlalchemy import select
    res = await db.execute(select(Review).where(Review.id == id))
    r = res.scalars().first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    from app.repositories.booking_repo import BookingRepo
    booking = await BookingRepo(db).get_by_id(r.booking_id)
    if booking.user_id == user.id or user.role.name == 'admin' or user.role == 'admin':
        await db.delete(r)
        await db.commit()
        return {'msg': 'deleted'}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

