from typing import Any, Dict, AnyStr, List, Optional
from app.db.results.schemas import ResultOut
from pydantic import BaseModel
from datetime import datetime
from app.db.enums import MetricsType
from app.db.users.schemas import UserName


class MeasurementBase(BaseModel):
    id: int = None
    value: float = None
    objective_id: int
    created_at: datetime = None
    updated_at: datetime = None
    created_by: int = None
    updated_by: int = None


class MeasurementEdit(MeasurementBase):
    class Config:
        orm_mode = True


class MeasurementOut(MeasurementBase):
    class Config:
        orm_mode = True
