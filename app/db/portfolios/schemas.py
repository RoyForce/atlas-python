from typing import List
from app.db.programs.schemas import ProgramBase
from pydantic import BaseModel
from datetime import datetime


class PortfolioBase(BaseModel):
    name: str
    team_id: int = None
    is_active: int = None
    description: str = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None


class PortfolioOut(PortfolioBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    programs: List[ProgramBase] = []

    class Config:
        orm_mode = True


class PortfolioCreate(PortfolioBase):
    name: str
    team_id: int = None
    description: str = None
    created_by: int = None
    updated_by: int = None

    class Config:
        orm_mode = True


class PortfolioEdit(PortfolioBase):
    id: int

    class Config:
        orm_mode = True
