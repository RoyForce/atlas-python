from pydantic import BaseModel
import typing as t


class LessonBase(BaseModel):
    name: str = None
    description: str = None
    duration: int = None
    page_content: str = None


class LessonOut(LessonBase):
    pass


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
