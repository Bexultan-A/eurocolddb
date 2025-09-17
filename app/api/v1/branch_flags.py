from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.branch_flag import (
    BranchFlagCreate, BranchFlagUpdate, BranchFlagOut, BranchFlagsPage
)
from app.services.branch_flag_service import branch_flag_service

router = APIRouter(prefix="/branch-flags", tags=["branch_flags"])

@router.post("", response_model=BranchFlagOut, status_code=status.HTTP_201_CREATED)
async def create_flag(payload: BranchFlagCreate, db: AsyncSession = Depends(get_db)):
    return await branch_flag_service.create(db, payload.model_dump())

@router.get("/{flag_id}", response_model=BranchFlagOut)
async def get_flag(flag_id: int, db: AsyncSession = Depends(get_db)):
    obj = await branch_flag_service.get(db, flag_id)
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.patch("/{flag_id}", response_model=BranchFlagOut)
async def update_flag(flag_id: int, payload: BranchFlagUpdate, db: AsyncSession = Depends(get_db)):
    obj = await branch_flag_service.update(db, flag_id, payload.model_dump(exclude_unset=True))
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.delete("/{flag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flag(flag_id: int, db: AsyncSession = Depends(get_db)):
    ok = await branch_flag_service.delete(db, flag_id)
    if not ok: raise HTTPException(404, "Not found")

@router.get("", response_model=BranchFlagsPage)
async def list_flags(
    branch: Optional[str] = None,
    region: Optional[str] = None,
    request: Optional[bool] = Query(None),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("id", pattern="^(id|branch|region)$"),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    total, items = await branch_flag_service.list(
        db, branch=branch, region=region, request=request,
        limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir
    )
    return {"meta": {"total": total, "limit": limit, "offset": offset}, "items": items}

@router.post("/{flag_id}/toggle", response_model=BranchFlagOut)
async def toggle_flag(flag_id: int, db: AsyncSession = Depends(get_db)):
    obj = await branch_flag_service.toggle(db, flag_id)
    if not obj: raise HTTPException(404, "Not found")
    return obj
