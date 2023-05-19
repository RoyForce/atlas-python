from typing import Any, Dict, AnyStr
from pydantic import BaseModel
from datetime import datetime


class ScreenObjectBase(BaseModel):
    name: str = None
    description: str = None
    properties: Dict[AnyStr, Any] = None
    screen_id: int = None


class ScreenObjectEdit(ScreenObjectBase):
    class Config:
        orm_mode = True


class ScreenObjectOut(ScreenObjectBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
