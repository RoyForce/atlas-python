from pydantic import BaseModel
from datetime import datetime


class ApplicationUrlBase(BaseModel):
    name: str
    description: str = None
    url: str = None
    created_at: datetime = None
    updated_at: datetime = None


class ApplicationUrlCreate(ApplicationUrlBase):
    class Config:
        orm_mode = True


class ApplicationUrlEdit(ApplicationUrlBase):
    class Config:
        orm_mode = True


class ApplicationUrl(ApplicationUrlBase):
    id: int

    class Config:
        orm_mode = True
