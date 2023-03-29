from typing import Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.db.jobs.schemas import JobOut


class ScreenBase(BaseModel):
    name: str = None
    description: str = None
    screen_url: str = None
    created_at: datetime = None
    updated_at: datetime = None


class ScreenEdit(ScreenBase):
    job_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class ScreenOut(ScreenBase):
    id: int
    job_ids: Optional[List[int]] = []
    jobs: List[JobOut] = []
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
