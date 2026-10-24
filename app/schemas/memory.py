from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class MemoryBase(BaseModel):
    query: str
    solution: Optional[str] = None


class MemoryCreate(MemoryBase):
    pass


class MemoryResponse(MemoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
