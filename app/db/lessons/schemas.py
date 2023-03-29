from pydantic import BaseModel
from datetime import datetime


class LessonBase(BaseModel):
    name: str = None
    description: str = None
    duration: int = None
    is_template: bool = None
    created_at: datetime = None
    updated_at: datetime = None


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

    class Config:
        orm_mode = True
