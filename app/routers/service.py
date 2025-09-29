from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional
from app.deps import get_db_session, require_admin
from app.repositories.service_repo import ServiceRepo
from app.schemas.service import ServiceCreate, ServiceOut
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get('/list_services', response_model=list[ServiceOut])
async def list_services(q: Optional[str] = None, price_min: Optional[float] = None, price_max: Optional[float] = None, active: Optional[bool] = None, db: AsyncSession = Depends(get_db_session)):
    repo = ServiceRepo(db)
    items = await repo.list(q=q, price_min=price_min, price_max=price_max, active=active)
    return items

@router.get('/{id}', response_model=ServiceOut)
async def get_service(id: int, db: AsyncSession = Depends(get_db_session)):
    repo = ServiceRepo(db)
    s = await repo.get(id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return s

@router.post('/', response_model=ServiceOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_service(payload: ServiceCreate, db: AsyncSession = Depends(get_db_session)):
    repo = ServiceRepo(db)
    s = await repo.create(**payload.model_dump())
    return s

@router.patch('/{id}', response_model=ServiceOut, dependencies=[Depends(require_admin)])
async def update_service(id: int, payload: ServiceCreate, db: AsyncSession = Depends(get_db_session)):
    repo = ServiceRepo(db)
    s = await repo.get(id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await repo.update(s, **payload.model_dump())

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_service(id: int, db: AsyncSession = Depends(get_db_session)):
    repo = ServiceRepo(db)
    s = await repo.get(id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await repo.delete(s)
    return
