from typing import Any, Dict, AnyStr
from pydantic import BaseModel
from datetime import datetime


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

    class Config:
        orm_mode = True
