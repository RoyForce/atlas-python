from ctypes import Union
from pydantic import BaseModel
from app.db.roles.schemas import Role
from typing import List
from datetime import datetime
from typing import Union


class PlaybookBase(BaseModel):
    name: str = None
    description: str = None
    page_content: str = None


class PlaybookCreate(PlaybookBase):
    name: str
    role_ids: List[int] = []

    class Config:
        orm_mode = True


class PlaybookEdit(PlaybookBase):
    role_ids: List[int] = []

    class Config:
        orm_mode = True


class Playbook(PlaybookBase):
    id: int
    roles: List[Role] = None
    role_ids: List[int] = []
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True
