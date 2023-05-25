from typing import List
from app.db.teams.schemas import TeamOut
from pydantic import BaseModel
from datetime import datetime


class ProgramBase(BaseModel):
    name: str
    team_id: int = None
    portfolio_id: int = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None


class ProgramOut(ProgramBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    teams: List[TeamOut] = []

    class Config:
        orm_mode = True


class ProgramCreate(ProgramBase):
    created_by: int = None

    class Config:
        orm_mode = True


class ProgramEdit(ProgramBase):
    id: int
    updated_by: int = None

    class Config:
        orm_mode = True
