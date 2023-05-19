from typing import List, Optional
from app.db.application_types.schemas import ApplicationTypeOut
from app.db.screen_objects.schemas import ScreenObjectOut
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
    application_type_id: int = None

    class Config:
        orm_mode = True


class ScreenOut(ScreenBase):
    id: int
    job_ids: Optional[List[int]] = []
    jobs: List[JobOut] = []
    created_at: datetime = None
    updated_at: datetime = None
    application_type_id: int = None
    application_type: ApplicationTypeOut = None
    objects: List[ScreenObjectOut] = []

    class Config:
        orm_mode = True
