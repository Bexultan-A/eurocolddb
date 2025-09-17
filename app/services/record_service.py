from typing import Optional, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.record_repo import RecordRepository
from app.models.record import Record

repo = RecordRepository()

class RecordService:

    async def create(self, db: AsyncSession, data: dict) -> Record:
        return await repo.create(db, data)

    async def get(self, db: AsyncSession, record_id: int) -> Record | None:
        return await repo.get(db, record_id)

    async def update(self, db: AsyncSession, record_id: int, data: dict) -> Record | None:
        rec = await repo.get(db, record_id)
        if not rec:
            return None
        return await repo.update(db, rec, data)

    async def delete(self, db: AsyncSession, record_id: int) -> bool:
        rec = await repo.get(db, record_id)
        if not rec:
            return False
        await repo.delete(db, rec)
        return True

    async def list(
        self, db: AsyncSession, **kwargs
    ) -> Tuple[int, Sequence[Record]]:
        return await repo.list(db, **kwargs)

    async def search(
        self, db: AsyncSession, **kwargs
    ) -> Tuple[int, Sequence[Record]]:
        return await repo.search(db, **kwargs)

service = RecordService()
