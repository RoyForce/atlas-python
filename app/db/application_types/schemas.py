from pydantic import BaseModel
from datetime import datetime


class ApplicationTypeBase(BaseModel):
    name: str
    description: str = None
    url: str = None


class ApplicationTypeOut(ApplicationTypeBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
