from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.lessons.crud import (
    get_lessons,
    get_lesson,
    create_lesson,
    delete_lesson,
    edit_lesson,
)
from app.db.lessons.schemas import LessonCreate, LessonEdit, Lesson, LessonOut

lesson_router = r = APIRouter()


@r.get(
    "/lessons",
    response_model=t.List[Lesson],
    response_model_exclude_none=True,
)
async def lessons_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all lessons
    """
    lessons = get_lessons(db)
    response.headers["Content-Range"] = f"0-9/{len(lessons)}"
    return lessons


@r.get(
    "/lessons/{lesson_id}",
    response_model=Lesson,
    response_model_exclude_none=True,
)
async def lesson_details(
    lesson_id: int,
    db=Depends(get_db),
):
    """
    Get any lesson details
    """
    lesson = get_lesson(db, lesson_id)
    return lesson


@r.post("/lessons", response_model=Lesson, response_model_exclude_none=True)
async def lesson_create(
    lesson: LessonCreate,
    db=Depends(get_db),
):
    """
    Create a new lesson
    """
    return create_lesson(db, lesson)


@r.put(
    "/lessons/{lesson_id}",
    response_model=Lesson,
    response_model_exclude_none=True,
)
async def lesson_edit(
    lesson_id: int,
    lesson: LessonEdit,
    db=Depends(get_db),
):
    """
    Update existing lesson
    """
    return edit_lesson(db, lesson_id, lesson)


@r.delete(
    "/lessons/{lesson_id}",
    response_model=Lesson,
    response_model_exclude_none=True,
)
async def lesson_delete(
    lesson_id: int,
    db=Depends(get_db),
):
    """
    Delete existing lesson
    """
    return delete_lesson(db, lesson_id)
