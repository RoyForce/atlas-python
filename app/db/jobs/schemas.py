from ctypes import Union
from pydantic import BaseModel, Field
import typing as t


class JobBase(BaseModel):
    name: str = None
    description: str = None
    is_locked: bool = None
    application_url_id: int = None
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


class Jobs(JobBase):
    id: int

    class Config:
        orm_mode = True
