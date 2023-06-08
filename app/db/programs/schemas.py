from typing import List
from app.db.teams.schemas import TeamOut
from pydantic import BaseModel
from datetime import datetime


class ProgramBase(BaseModel):
    id: int
    name: str
    description: str = None
    portfolio_id: int = None
    team_id: int = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class ProgramOut(ProgramBase):
    teams: List[TeamOut] = []

    class Config:
        orm_mode = True


class ProgramEdit(BaseModel):
    name: str
    description: str = None
    portfolio_id: int = None

    class Config:
        orm_mode = True
