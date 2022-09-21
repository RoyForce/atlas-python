from ctypes import Union
from pydantic import BaseModel, Field
import typing as t
from app.db.roles.schemas import Role
from typing import List


class PlaybookBase(BaseModel):
    name: str = None
    description: str = None
    page_content: str = None
    roles: List[Role] = None


class PlaybookOut(PlaybookBase):
    pass


class PlaybookCreate(PlaybookBase):
    name: str

    class Config:
        orm_mode = True


class PlaybookEdit(PlaybookBase):
    class Config:
        orm_mode = True


class Playbook(PlaybookBase):
    id: int

    class Config:
        orm_mode = True
