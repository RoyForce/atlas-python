from pydantic import BaseModel
from datetime import datetime


class PortfolioBase(BaseModel):
    title: str
    team_id: int = None
    is_active: int = None
    description: str = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None
    created_at: datetime = None
    updated_at: datetime = None


class PortfolioOut(PortfolioBase):
    id: int

    class Config:
        orm_mode = True


class PortfolioCreate(PortfolioBase):
    title: str
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
