from pydantic import BaseModel
from datetime import datetime
from typing import List, Any, Dict, AnyStr, Optional


class CostCenterBase(BaseModel):
    name: str
    hr_rate: int = None
    description: str = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None


class CostCenterOut(CostCenterBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class CostCenterCreate(CostCenterBase):
    created_by: int = None

    class Config:
        orm_mode = True


class CostCenterEdit(CostCenterBase):
    id: int
    updated_by: int = None

    class Config:
        orm_mode = True
