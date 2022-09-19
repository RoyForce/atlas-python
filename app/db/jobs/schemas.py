from ctypes import Union
from pydantic import BaseModel, Field
import typing as t
from app.db.roles.schemas import Role
from typing import List


class JobBase(BaseModel):
    name: str = None
    description: str = None
    is_locked: bool = None
    application_url_id: int = None
    roles: List[Role] = None
    # steps: JSON = None


class JobOut(JobBase):
    pass


class JobCreate(JobBase):
    name: str

    class Config:
        orm_mode = True


class JobEdit(JobBase):
    class Config:
        orm_mode = True


class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
