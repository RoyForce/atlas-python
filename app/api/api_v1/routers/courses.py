from app.core.auth import get_current_active_user
from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.courses import models
from app.db.core import get_lists, get_item, delete_item
from app.db.courses.crud import (
    create_course,
    edit_course,
)
from app.db.courses.schemas import CourseCreate, CourseEdit, Course

courses_router = r = APIRouter()


@r.get(
    "/courses",
    response_model=t.List[Course],
    response_model_exclude_none=True,
)
async def courses_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get all courses
    """
    courses = get_lists(db, models.Course, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(courses)}"
    return courses


@r.get(
    "/courses/{course_id}",
    response_model=Course,
    response_model_exclude_none=True,
)
async def course_details(
    course_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get any course details
    """
    return get_item(db, models.Course, course_id)


@r.post("/courses", response_model=Course, response_model_exclude_none=True)
async def course_create(
    course: CourseCreate,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Create a new course
    """
    return create_course(db, course)


@r.put(
    "/courses/{course_id}",
    response_model=Course,
    response_model_exclude_none=True,
)
async def course_edit(
    course_id: int,
    course: CourseEdit,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Update existing course
    """
    return edit_course(db, course_id, course)


@r.delete(
    "/courses/{course_id}",
    response_model=Course,
    response_model_exclude_none=True,
)
async def course_delete(
    course_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Delete existing course
    """
    return delete_item(db, models.Course, course_id)
