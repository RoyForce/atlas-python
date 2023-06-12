from typing import Any, Dict, AnyStr, List, Optional
from app.db.results.schemas import ResultOut
from pydantic import BaseModel
from datetime import datetime
from app.db.enums import MetricsType
from app.db.users.schemas import UserName


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
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
