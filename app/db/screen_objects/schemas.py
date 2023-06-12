from typing import Any, Dict, AnyStr
from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class ScreenObjectBase(BaseModel):
    name: str = None
    description: str = None
    properties: Dict[AnyStr, Any] = None
    screen_id: int = None
    created_by: int = None
    updated_by: int = None


class ScreenObjectEdit(ScreenObjectBase):
    class Config:
        orm_mode = True


class ScreenObjectOut(ScreenObjectBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
