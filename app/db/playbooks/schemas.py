from pydantic import BaseModel
from app.db.roles.schemas import Role
from typing import List, Optional
from datetime import datetime


class PlaybookBase(BaseModel):
    name: str = None
    description: str = None
    page_content: str = None


class PlaybookEdit(PlaybookBase):
    role_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class PlaybookOut(PlaybookBase):
    id: int
    roles: List[Role] = None
    role_ids: Optional[List[int]] = []
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
