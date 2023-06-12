from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class LessonBase(BaseModel):
    name: str = None
    description: str = None
    duration: int = None
    is_template: bool = None
    created_at: datetime = None
    updated_at: datetime = None
    created_by: int = None
    updated_by: int = None


class LessonCreate(LessonBase):
    name: str
    page_content: str = None

    class Config:
        orm_mode = True


class LessonEdit(LessonBase):
    page_content: str = None

    class Config:
        orm_mode = True


class LessonOut(LessonBase):
    id: int
    page_content: str = None

    class Config:
        orm_mode = True


class LessonListOut(LessonBase):
    id: int
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
