from typing import Any, Dict, AnyStr, List
from app.db.results.schemas import ResultOut
from pydantic import BaseModel
from datetime import datetime
from app.db.enums import MetricsType


class ObjectiveBase(BaseModel):
    name: str = None
    description: str = None
    metrics_type: MetricsType = None
    start_value: float = None
    target_value: float = None
    created_by: int = None
    updated_by: int = None


class ObjectiveEdit(ObjectiveBase):
    class Config:
        orm_mode = True


class ObjectiveOut(ObjectiveBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    results: List[ResultOut] = []

    class Config:
        orm_mode = True
