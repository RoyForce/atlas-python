from pydantic import BaseModel
import typing as t
from typing import List, Any, Dict, AnyStr
from enum import Enum
from datetime import datetime
from app.db.users.schemas import UserName


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
    created_at: datetime = None
    updated_at: datetime = None
    created_by: int = None
    updated_by: int = None


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
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
