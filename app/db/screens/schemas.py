from pydantic import BaseModel
from datetime import datetime


class ScreenBase(BaseModel):
    name: str = None
    description: str = None
    created_at: datetime = None
    updated_at: datetime = None


class ScreenCreate(ScreenBase):
    class Config:
        orm_mode = True


class ScreenEdit(ScreenBase):
    class Config:
        orm_mode = True


class Screen(ScreenBase):
    id: int

    class Config:
        orm_mode = True
