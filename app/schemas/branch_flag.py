from pydantic import BaseModel
from typing import Optional

class BranchFlagBase(BaseModel):
    branch: str
    request: bool = False
    region: str

class BranchFlagCreate(BranchFlagBase):
    pass

class BranchFlagUpdate(BaseModel):
    branch: Optional[str] = None
    request: Optional[bool] = None
    region: Optional[str] = None

class BranchFlagOut(BranchFlagBase):
    id: int
    class Config:
        from_attributes = True

class BranchFlagsPage(BaseModel):
    meta: dict
    items: list[BranchFlagOut]
