from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
from datetime import datetime
from app.db.base import Base

class BranchFlag(Base):
    __tablename__ = "branch_flags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    branch: Mapped[str] = mapped_column(CITEXT, nullable=False)
    request: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    region: Mapped[str | None] = mapped_column(CITEXT, nullable=True)  # станет NOT NULL после импорта

    created_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
