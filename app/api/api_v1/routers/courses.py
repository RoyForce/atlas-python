from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.courses.crud import (
    get_courses,
    get_course,
    create_course,
    delete_course,
    edit_course,
)
from app.db.courses.schemas import CourseCreate, CourseEdit, Course, CourseOut
from app.core.auth import get_current_active_superuser

courses_router = r = APIRouter()


@r.get(
    "/courses",
    response_model=t.List[Course],
    response_model_exclude_none=True,
)
async def courses_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all courses
    """
    courses = get_courses(db)
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
):
    """
    Get any course details
    """
    course = get_course(db, course_id)
    return course


@r.post("/courses", response_model=Course, response_model_exclude_none=True)
async def course_create(
    course: CourseCreate,
    db=Depends(get_db),
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
):
    """
    Delete existing course
    """
    return delete_course(db, course_id)
