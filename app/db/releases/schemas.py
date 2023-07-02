from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class ProgramBase(BaseModel):
    id: int
    name: str
    description: str = None
    short_name: str = None
    portfolio_id: int = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None
    start_date: datetime = None
    end_date: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True


class ProgramOut(ProgramBase):
    class Config:
        orm_mode = True


class ProgramEdit(BaseModel):
    name: str
    description: str = None
    portfolio_id: int = None
    created_by: int = None
    updated_by: int = None

    class Config:
        orm_mode = True
