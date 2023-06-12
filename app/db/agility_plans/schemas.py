from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any
from app.db.enums import MetricsType


class AgilityPlanBase(BaseModel):
    name: str = None
    description: str = None

    created_at: datetime = None
    updated_at: datetime = None


class ObjectiveItemBase(BaseModel):
    id: int = None
    name: str = None
    description: str = None


class AgilityPlanCreate(AgilityPlanBase):
    name: str

    class Config:
        orm_mode = True


class AgilityPlanEdit(AgilityPlanBase):
    class Config:
        orm_mode = True


class AgilityPlanOut(AgilityPlanBase):
    id: int

    class Config:
        orm_mode = True


class AgilityPlanListOut(AgilityPlanBase):
    id: int

    class Config:
        orm_mode = True
