from app.db.users.schemas import User
from pydantic import BaseModel
from datetime import datetime
from typing import List, Any, Dict, AnyStr, Optional


class TeamBase(BaseModel):
    name: str
    program_id: int = None
    type: int = None
    is_active: bool = True
    description: str = None
    sprint_prefix: str = None
    short_name: str = None
    source_id: int = None
    source_update_at: datetime = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None
    user_ids: Optional[List[int]] = []


class TeamOut(TeamBase):
    id: int
    users: List[User] = []
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class TeamCreate(TeamBase):
    created_by: int = None

    class Config:
        orm_mode = True


class TeamEdit(TeamBase):
    id: int
    updated_by: int = None

    class Config:
        orm_mode = True
