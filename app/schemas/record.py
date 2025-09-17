from pydantic import BaseModel, field_validator
from typing import Optional
from app.utils.phone import normalize_phone_e164

class RecordBase(BaseModel):
    master_name: Optional[str] = None
    reminder: Optional[int] = None

    client_full_name: Optional[str] = None
    phone_raw: Optional[str] = None
    phone_e164: Optional[str] = None

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

    @field_validator("phone_e164", mode="before")
    @classmethod
    def _norm_phone(cls, v):
        return normalize_phone_e164(v)

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    master_name: Optional[str] = None
    reminder: Optional[int] = None

    client_full_name: Optional[str] = None
    phone_raw: Optional[str] = None
    phone_e164: Optional[str] = None

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

    @field_validator("phone_e164", mode="before")
    @classmethod
    def _norm_phone(cls, v):
        return normalize_phone_e164(v)

class RecordOut(RecordBase):
    id: int
    class Config:
        from_attributes = True

class RecordsPage(BaseModel):
    meta: "PageMeta"
    items: list[RecordOut]

from app.schemas.common import PageMeta
RecordsPage.model_rebuild()
