from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, Text
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from app.db.base import Base

class Record(Base):
    __tablename__ = "records"

    id: Mapped[int]                  = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    master_name: Mapped[str | None]  = mapped_column(CITEXT, nullable=True)
    reminder: Mapped[int | None]     = mapped_column(Integer, nullable=True)

    client_full_name: Mapped[str | None] = mapped_column(CITEXT, nullable=True)
    contact_number: Mapped[str | None]    = mapped_column(Text, nullable=True)
    phone: Mapped[str | None]             = mapped_column(Text, nullable=True)

    city: Mapped[str | None]         = mapped_column(CITEXT, nullable=True)
    branch: Mapped[str | None]       = mapped_column(CITEXT, nullable=True)

    reason: Mapped[str | None]       = mapped_column(CITEXT, nullable=True)
    problem: Mapped[str | None]      = mapped_column(CITEXT, nullable=True)

    external_id: Mapped[str | None]  = mapped_column(Text, nullable=True)
    chat_id: Mapped[str | None]      = mapped_column(Text, nullable=True)

    ticket_number: Mapped[str | None]= mapped_column(CITEXT, nullable=True)
    language: Mapped[str | None]     = mapped_column(CITEXT, nullable=True)
    messenger: Mapped[str | None]    = mapped_column(CITEXT, nullable=True)
    region: Mapped[str]              = mapped_column(CITEXT, nullable=False)

    created_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
