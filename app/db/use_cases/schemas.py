from pydantic import BaseModel
from app.db.roles.schemas import Role
from app.db.jobs.schemas import JobOut
from typing import List, Optional
from datetime import datetime


class UseCaseBase(BaseModel):
    name: str = None
    description: str = None
    table_config: str = None


class UseCaseCreate(UseCaseBase):
    role_ids: Optional[List[int]] = []
    job_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class UseCaseEdit(UseCaseBase):
    role_ids: Optional[List[int]] = []
    job_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class UseCaseOut(UseCaseBase):
    id: int
    role_ids: Optional[List[int]] = []
    job_ids: Optional[List[int]] = []
    jobs: List[JobOut] = []
    roles: List[Role] = []
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
