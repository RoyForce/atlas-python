from typing import Any, Dict, AnyStr
from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class QuestionBase(BaseModel):
    name: str = None
    description: str = None
    dimension_id: int = None
    created_by: int = None
    updated_by: int = None


class QuestionEdit(QuestionBase):
    class Config:
        orm_mode = True


class QuestionOut(QuestionBase):
    id: int
    created_by: int = None
    updated_by: int = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
