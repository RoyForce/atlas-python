from pydantic import BaseModel
from datetime import datetime


class ActionBase(BaseModel):
    name: str = None
    description: str = None
    action_type: str = None
    created_at: datetime = None
    updated_at: datetime = None


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

    class Config:
        orm_mode = True
