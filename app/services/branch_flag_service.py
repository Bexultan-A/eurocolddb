from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence, Tuple
from app.repositories.branch_flag_repo import repo_branch_flag
from app.models.branch_flag import BranchFlag

class BranchFlagService:
    async def create(self, db: AsyncSession, data: dict) -> BranchFlag:
        return await repo_branch_flag.create(db, data)

    async def get(self, db: AsyncSession, flag_id: int) -> BranchFlag | None:
        return await repo_branch_flag.get(db, flag_id)

    async def update(self, db: AsyncSession, flag_id: int, data: dict) -> BranchFlag | None:
        obj = await repo_branch_flag.get(db, flag_id)
        if not obj: return None
        return await repo_branch_flag.update(db, obj, data)

    async def delete(self, db: AsyncSession, flag_id: int) -> bool:
        obj = await repo_branch_flag.get(db, flag_id)
        if not obj: return False
        await repo_branch_flag.delete(db, obj)
        return True

    async def list(self, db: AsyncSession, **kwargs) -> Tuple[int, Sequence[BranchFlag]]:
        return await repo_branch_flag.list(db, **kwargs)

    async def toggle(self, db: AsyncSession, flag_id: int) -> BranchFlag | None:
        obj = await repo_branch_flag.get(db, flag_id)
        if not obj: return None
        return await repo_branch_flag.toggle(db, obj)

branch_flag_service = BranchFlagService()
