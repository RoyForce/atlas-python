from pydantic import BaseModel
from datetime import datetime


class LessonBase(BaseModel):
    name: str = None
    description: str = None
    duration: int = None
    page_content: str = None
    is_template: bool = None
    created_at: datetime = None
    updated_at: datetime = None


class LessonCreate(LessonBase):
    name: str

    class Config:
        orm_mode = True


class LessonEdit(LessonBase):
    class Config:
        orm_mode = True


class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True
