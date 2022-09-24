from ctypes import Union
from email.mime import application
from pydantic import BaseModel, Field
import typing as t
from app.db.roles.schemas import Role
from app.db.applicationurls.schemas import ApplicationUrl
from typing import List, Any, Dict, AnyStr


class JobBase(BaseModel):
    name: str = None
    description: str = None
    is_locked: bool = None
    steps: Dict[AnyStr, Any] = None


class JobOut(JobBase):
    application_url: ApplicationUrl = None
    roles: List[Role] = None
    pass


class JobCreate(JobBase):
    name: str
    application_url_id: int = None
    role_ids: List[int] = []

    class Config:
        orm_mode = True


class JobEdit(JobBase):
    application_url_id: int = None
    role_ids: List[int] = []

    class Config:
        orm_mode = True


class Job(JobBase):
    id: int
    application_url: ApplicationUrl = None
    roles: List[Role] = None

    class Config:
        orm_mode = True
