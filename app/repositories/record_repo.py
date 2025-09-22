from typing import Sequence, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, literal_column, or_, text
from app.models.record import Record
from app.core.config import settings

def _escape_like(s: str) -> str:
    # экранируем спецсимволы для LIKE/ILIKE
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

class RecordRepository:

    # -------- CRUD --------
    async def create(self, db: AsyncSession, data: dict) -> Record:
        rec = Record(**data)
        db.add(rec)
        await db.flush()
        await db.refresh(rec)
        return rec

    async def get(self, db: AsyncSession, record_id: int) -> Optional[Record]:
        res = await db.execute(select(Record).where(Record.id == record_id))
        return res.scalar_one_or_none()

    async def update(self, db: AsyncSession, rec: Record, data: dict) -> Record:
        for k, v in data.items():
            setattr(rec, k, v)
        await db.flush()
        await db.refresh(rec)
        return rec

    async def delete(self, db: AsyncSession, rec: Record) -> None:
        await db.delete(rec)

    # -------- List + filters --------
    async def list(
        self, db: AsyncSession,
        *, region=None, city=None, branch=None,
        language=None, messenger=None,
        ticket_number: str | None = None,
        external_id: str | None = None,
        sort_by="id", sort_dir="desc",
        limit=20, offset=0
    ):
        stmt = select(Record)

        if region:
            stmt = stmt.where(Record.region == region)
        if city:
            stmt = stmt.where(Record.city == city)
        if branch:
            stmt = stmt.where(Record.branch == branch)
        if language:
            stmt = stmt.where(Record.language == language)
        if messenger:
            stmt = stmt.where(Record.messenger == messenger)

        # >>> НОВОЕ: префиксный поиск
        if ticket_number:
            esc = _escape_like(ticket_number.strip())
            stmt = stmt.where(Record.ticket_number.ilike(f"{esc}%", escape="\\"))

        if external_id:
            esc = _escape_like(external_id.strip())
            stmt = stmt.where(Record.external_id.ilike(f"{esc}%", escape="\\"))

        sortable = {
            "id": Record.id,
            "created_at": Record.created_at,
            "updated_at": Record.updated_at,
            "ticket_number": Record.ticket_number,
            "external_id": Record.external_id,
        }
        col = sortable.get(sort_by, Record.id)
        stmt = stmt.order_by(col.desc() if sort_dir == "desc" else col.asc())

        total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
        items = (await db.execute(stmt.limit(limit).offset(offset))).scalars().all()
        return total, items

    # -------- Search --------
    async def search(
        self,
        db: AsyncSession,
        *,
        q: str,
        region: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[int, Sequence[Record]]:
        where = []
        if region:
            where.append(Record.region == region)

        # FTS + ILIKE поля (ускоряются триграммными индексами)
        ts_cond = text(f"search_vector @@ websearch_to_tsquery('{settings.FTS_DICTIONARY}', :tsq)")
        ilike_fields = [
            Record.client_full_name, Record.master_name, Record.reason,
            Record.problem, Record.city, Record.branch, Record.language,
            Record.messenger, Record.ticket_number, Record.external_id, Record.phone, Record.contact_number,
        ]
        ilike_cond = or_(*[f.ilike(f"%{q}%") for f in ilike_fields])

        base = (
            select(Record)
            .where(*where)
            .where(or_(ts_cond, ilike_cond))
            .order_by(Record.id.desc())
            .params(tsq=q)
        )

        # count
        total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()

        # page
        items = (await db.execute(base.limit(limit).offset(offset))).scalars().all()
        return total, items
