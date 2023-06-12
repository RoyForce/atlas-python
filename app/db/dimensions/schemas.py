from typing import Any, Dict, AnyStr, List
from app.db.questions.schemas import QuestionOut
from typing import Any, Dict, AnyStr
from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class DimensionBase(BaseModel):
    name: str = None
    description: str = None
    assessment_id: int = None
    baseline_value: int = None
    ideal_value: int = None
    created_by: int = None
    updated_by: int = None


class DimensionEdit(DimensionBase):
    class Config:
        orm_mode = True


class DimensionOut(DimensionBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    questions: List[QuestionOut] = []
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
