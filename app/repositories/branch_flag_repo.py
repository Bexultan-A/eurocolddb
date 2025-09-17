from typing import Optional, Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.branch_flag import BranchFlag

class BranchFlagRepository:
    async def create(self, db: AsyncSession, data: dict) -> BranchFlag:
        obj = BranchFlag(**data)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def get(self, db: AsyncSession, flag_id: int) -> BranchFlag | None:
        res = await db.execute(select(BranchFlag).where(BranchFlag.id == flag_id))
        return res.scalar_one_or_none()

    async def update(self, db: AsyncSession, obj: BranchFlag, data: dict) -> BranchFlag:
        for k, v in data.items():
            setattr(obj, k, v)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, obj: BranchFlag) -> None:
        await db.delete(obj)

    async def list(
        self, db: AsyncSession,
        *, branch: Optional[str] = None, request: Optional[bool] = None, region: Optional[str] = None,
        limit: int = 20, offset: int = 0, sort_by: str = "id", sort_dir: str = "desc"
    ) -> Tuple[int, Sequence[BranchFlag]]:
        stmt = select(BranchFlag)
        if branch:
            stmt = stmt.where(BranchFlag.branch == branch)
        if region:
            stmt = stmt.where(BranchFlag.region == region)
        if request is not None:
            stmt = stmt.where(BranchFlag.request == request)

        sortable = {"id": BranchFlag.id, "branch": BranchFlag.branch, "region": BranchFlag.region}
        col = sortable.get(sort_by, BranchFlag.id)
        stmt = stmt.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
        items = (await db.execute(stmt.limit(limit).offset(offset))).scalars().all()
        return total, items

    async def toggle(self, db: AsyncSession, obj: BranchFlag) -> BranchFlag:
        obj.request = not obj.request
        await db.flush()
        await db.refresh(obj)
        return obj

repo_branch_flag = BranchFlagRepository()
