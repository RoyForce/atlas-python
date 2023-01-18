from app.core.auth import get_current_active_user
from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.lessons import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.lessons.schemas import LessonCreate, LessonEdit, Lesson

lesson_router = r = APIRouter()


@r.get(
    "/lessons",
    response_model=t.List[Lesson],
    response_model_exclude_none=True,
)
async def lessons_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get all lessons
    """
    lessons = get_lists(db, models.Lesson, request.query_params)
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
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get any lesson details
    """
    return get_item(db, models.Lesson, lesson_id)


@r.post("/lessons", response_model=Lesson, response_model_exclude_none=True)
async def lesson_create(
    lesson: LessonCreate,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Create a new lesson
    """
    return create_item(db, models.Lesson, lesson)


@r.put(
    "/lessons/{lesson_id}",
    response_model=Lesson,
    response_model_exclude_none=True,
)
async def lesson_edit(
    lesson_id: int,
    lesson: LessonEdit,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Update existing lesson
    """
    return edit_item(db, models.Lesson, lesson_id, lesson)


@r.delete(
    "/lessons/{lesson_id}",
    response_model=Lesson,
    response_model_exclude_none=True,
)
async def lesson_delete(
    lesson_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Delete existing lesson
    """
    return delete_item(db, models.Lesson, lesson_id)
