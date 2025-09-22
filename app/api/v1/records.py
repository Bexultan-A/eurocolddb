from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.record import RecordCreate, RecordUpdate, RecordOut, RecordsPage
from app.schemas.common import PageMeta
from app.services.record_service import service

router = APIRouter(prefix="/records", tags=["records"])

# -------- CRUD --------
@router.post("", response_model=RecordOut, status_code=status.HTTP_201_CREATED)
async def create_record(payload: RecordCreate, db: AsyncSession = Depends(get_db)):
    rec = await service.create(db, payload.model_dump())
    return rec

# -------- List + filters + сортировка --------
@router.get("", response_model=RecordsPage)
async def list_records(
    region: Optional[str] = None,
    city: Optional[str] = None,
    branch: Optional[str] = None,
    language: Optional[str] = None,
    messenger: Optional[str] = None,
    ticket_number: Optional[str] = None,
    external_id: Optional[str] = None,
    sort_by: str = Query("id", pattern="^(id|created_at|updated_at|ticket_number|external_id)$"),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    total, items = await service.list(
        db,
        region=region, city=city, branch=branch,
        language=language, messenger=messenger,
        ticket_number=ticket_number, external_id=external_id,
        sort_by=sort_by, sort_dir=sort_dir,
        limit=limit, offset=offset,
    )
    return {"meta": PageMeta(total=total, limit=limit, offset=offset), "items": items}

# -------- Поиск --------
@router.get("/search", response_model=RecordsPage)
async def search_records(
    q: str = Query(..., min_length=1),
    region: Optional[str] = None,
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    total, items = await service.search(db, q=q, region=region, limit=limit, offset=offset)
    return {"meta": PageMeta(total=total, limit=limit, offset=offset), "items": items}


@router.get("/{record_id}", response_model=RecordOut)
async def get_record(record_id: int, db: AsyncSession = Depends(get_db)):
    rec = await service.get(db, record_id)
    if not rec:
        raise HTTPException(404, "Record not found")
    return rec

@router.patch("/{record_id}", response_model=RecordOut)
async def update_record(record_id: int, payload: RecordUpdate, db: AsyncSession = Depends(get_db)):
    rec = await service.update(db, record_id, payload.model_dump(exclude_unset=True))
    if not rec:
        raise HTTPException(404, "Record not found")
    return rec

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(record_id: int, db: AsyncSession = Depends(get_db)):
    ok = await service.delete(db, record_id)
    if not ok:
        raise HTTPException(404, "Record not found")
