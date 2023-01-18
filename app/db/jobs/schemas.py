from ctypes import Union
from email.mime import application
from pydantic import BaseModel, Field
import typing as t
from app.db.roles.schemas import Role
from app.db.application_urls.schemas import ApplicationUrl
from typing import List, Any, Dict, AnyStr
from enum import Enum


class JobBase(BaseModel):
    name: str = None
    description: str = None
    is_locked: bool = None
    steps: Dict[AnyStr, Any] = None
    is_template: bool = None


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
    role_ids: List[int] = []
    application_url_id: int = None

    class Config:
        orm_mode = True


class ExtensionMode(str, Enum):
    """The possible modes for extension"""

    DESIGNER = "D"
    EXECUTOR = "E"
