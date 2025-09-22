from pydantic import BaseModel
from typing import Optional

class RecordBase(BaseModel):
    master_name: Optional[str] = None
    reminder: Optional[int] = None

    client_full_name: Optional[str] = None
    contact_number: Optional[str] = None
    phone: Optional[str] = None

    city: Optional[str] = None
    branch: Optional[str] = None

    reason: Optional[str] = None
    problem: Optional[str] = None

    external_id: Optional[str] = None
    chat_id: Optional[str] = None

    ticket_number: Optional[str] = None
    language: Optional[str] = None
    messenger: Optional[str] = None
    region: str

    message_id: Optional[int] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    master_name: Optional[str] = None
    reminder: Optional[int] = None

    client_full_name: Optional[str] = None
    contact_number: Optional[str] = None
    phone: Optional[str] = None

    city: Optional[str] = None
    branch: Optional[str] = None

    reason: Optional[str] = None
    problem: Optional[str] = None

    external_id: Optional[str] = None
    chat_id: Optional[str] = None

    ticket_number: Optional[str] = None
    language: Optional[str] = None
    messenger: Optional[str] = None
    region: Optional[str] = None

    message_id: Optional[int] = None

class RecordOut(RecordBase):
    id: int
    class Config:
        from_attributes = True

class RecordsPage(BaseModel):
    meta: "PageMeta"
    items: list[RecordOut]

from app.schemas.common import PageMeta
RecordsPage.model_rebuild()
