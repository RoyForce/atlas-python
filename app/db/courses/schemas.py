from pydantic import BaseModel
import typing as t
from typing import List, Any, Dict, AnyStr
from enum import Enum


class ItemsEnum(str, Enum):
    SECTION = "SECTION"
    LESSON = "LESSON"
    QUIZ = "QUIZ"


class CourseItemBase(BaseModel):
    id: int = None
    item_type: ItemsEnum = None
    item_title: str = None
    item_id: int = None
    item_order: int = None

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str = None
    description: str = None
    duration: int = None
    enroll_required: bool = None
    passing_percentage: int = None
    items: Any = None


class CourseOut(CourseItemBase):
    # items: List[CourseItemBase] = None
    pass


class CourseCreate(CourseBase):
    name: str
    items: List[CourseItemBase] = None

    class Config:
        orm_mode = True


class CourseEdit(CourseBase):
    items: List[CourseItemBase] = None

    class Config:
        orm_mode = True


class Course(CourseBase):
    id: int
    items: List[CourseItemBase] = None

    class Config:
        orm_mode = True
