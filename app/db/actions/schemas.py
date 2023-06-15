from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class ActionBase(BaseModel):
    id: int
    name: str = None
    description: str = None
    action_type: str = None
    created_by: int = None
    updated_by: int = None


class ActionCreate(ActionBase):
    name: str
    action_type: str = None

    class Config:
        orm_mode = True


class ActionEdit(ActionBase):
    action_type: str = None

    class Config:
        orm_mode = True


class ActionOut(ActionBase):
    id: int
    action_type: str = None

    class Config:
        orm_mode = True


class ActionListOut(ActionBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
