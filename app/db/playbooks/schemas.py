from pydantic import BaseModel
from app.db.roles.schemas import Role
from typing import List, Optional
from datetime import datetime


class PlaybookBase(BaseModel):
    name: str = None
    description: str = None


class PlaybookEdit(PlaybookBase):
    role_ids: Optional[List[int]] = []
    page_content: str = None

    class Config:
        orm_mode = True


class PlaybookOut(PlaybookBase):
    id: int
    roles: List[Role] = None
    role_ids: Optional[List[int]] = []
    page_content: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class PlaybookListOut(PlaybookBase):
    id: int
    roles: List[Role] = None
    role_ids: Optional[List[int]] = []
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
