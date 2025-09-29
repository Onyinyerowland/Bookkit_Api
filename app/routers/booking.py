from fastapi import APIRouter, Depends, HTTPException, Query
from app.deps import get_current_user, get_db_session, require_admin
from app.schemas.booking import BookingCreate, BookingOut, BookingUpdate
from app.services.booking_service import BookingService
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.service_repo import ServiceRepo
from datetime import datetime
from app.repositories.booking_repo import BookingRepo

router = APIRouter()



@router.post('/', status_code=201)
async def create_booking(payload: BookingCreate, user = Depends(get_current_user), db = Depends(get_db_session)):
    svc = BookingService(db)
    try:
        booking = await svc.create(str(user.id), str(payload.service_id), payload.start_time)
        return booking
    except ValueError as e:
        if str(e) == 'service_not_found':
            raise HTTPException(404, 'Service not found')
        if str(e) == 'slot_conflict':
            raise HTTPException(409, 'Requested slot conflicts with existing booking')
        raise


@router.get('/', response_model=list[BookingOut])
async def list_bookings(status: str | None = Query(None), from_dt: datetime | None = Query(None), to_dt: datetime | None = Query(None), user = Depends(get_current_user), db = Depends(get_db_session)):
    svc = BookingService(db)
    if user.role.value == 'admin':
        return await svc.list_all(status, from_dt, to_dt)
    return await svc.list_for_user(str(user.id))


@router.get('/{id}')
async def get_booking(id: str, user = Depends(get_current_user), db = Depends(get_db_session)):
    svc = BookingService(db)
    booking = await svc.get(id)
    if not booking: raise HTTPException(404, 'Not found')
    if str(booking.user_id) != str(user.id) and user.role.value != 'admin':
        raise HTTPException(403, 'Forbidden')
    return booking


@router.delete('/{id}')
async def delete_booking(id: str, user = Depends(get_current_user), db = Depends(get_db_session)):
    svc = BookingService(db)
    booking = await svc.get(id)
    if not booking: raise HTTPException(404, 'Not found')
    if user.role.value == 'admin':
        await svc.delete(booking)
        return {'detail':'deleted'}
    if str(booking.user_id) != str(user.id): raise HTTPException(403, 'Forbidden')
    # only allow delete before start_time
    if booking.start_time <= datetime.utcnow():
        raise HTTPException(400, 'Cannot delete booking after it has started')
    await svc.delete(booking)
    return {'detail':'deleted'}

@router.patch('/{id}')
async def patch_booking(id: str, payload: BookingUpdate, user = Depends(get_current_user), db = Depends(get_db_session)):
    svc = BookingService(db)
    booking = await svc.get(id)
    if not booking: raise HTTPException(404, 'Not found')
    if user.role.value == 'admin':
        if payload.status:
            booking = await svc.update(booking, status=payload.status)
            return booking
        raise HTTPException(400, 'Nothing to update')
# owner
    if str(booking.user_id) != str(user.id): raise HTTPException(403, 'Forbidden')
    if booking.status not in ('pending','confirmed'):
        raise HTTPException(400, 'Cannot modify booking in current status')
    if payload.start_time:
# reschedule: check overlap
        try:
            updated = await svc.update(booking, start_time=payload.start_time)
            return updated
        except ValueError as e:
            if str(e) == 'slot_conflict': raise HTTPException(409, 'Slot conflict')
    if payload.status == 'cancelled':
        updated = await svc.update(booking, status='cancelled')
        return updated
    raise HTTPException(400, 'Nothing to update')
