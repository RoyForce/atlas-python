from ctypes import Union
from pydantic import BaseModel, Field
import typing as t
from app.db.roles.schemas import Role
from app.db.jobs.schemas import Job
from typing import List


class UseCaseBase(BaseModel):
    name: str = None
    description: str = None
    table_config: str = None


class UseCaseOut(UseCaseBase):
    roles: List[Role] = None
    jobs: List[Job] = None


class UseCaseCreate(UseCaseBase):
    name: str
    role_ids: List[int] = []
    job_ids: List[int] = []

    class Config:
        orm_mode = True


class UseCaseEdit(UseCaseBase):
    role_ids: List[int] = []
    job_ids: List[int] = []

    class Config:
        orm_mode = True


class UseCase(UseCaseBase):
    id: int
    roles: List[Role] = None
    role_ids: List[int] = []
    jobs: List[Job] = None
    job_ids: List[int] = []

    class Config:
        orm_mode = True
