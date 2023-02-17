from pydantic import BaseModel
from datetime import datetime
from typing import Union


class ApplicationUrlBase(BaseModel):
    name: str
    description: str = None
    url: str = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


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
