from app.core.auth import get_current_active_user
from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.jobs import models
from app.db.session import get_db
from app.db.jobs.crud import (
    create_job,
    delete_job,
    edit_job,
    validate_extension_token,
    validate_user_and_job,
)
from app.db.jobs.schemas import (
    JobCreate,
    JobEdit,
    Job,
)
from app.db.core import get_lists, get_item

jobs_router = r = APIRouter()
extension_router = er = APIRouter()


@r.get(
    "/jobs",
    response_model=t.List[Job],
    response_model_exclude_none=True,
)
async def jobs_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get all Jobs
    """
    jobs = get_lists(db, models.Job, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(jobs)}"
    return jobs


@r.get(
    "/jobs/{job_id}",
    response_model=Job,
    response_model_exclude_none=True,
)
async def job_details(
    job_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get any job details
    """
    return get_item(db, models.Job, job_id)


@r.post("/jobs", response_model=Job, response_model_exclude_none=True)
async def job_create(
    job: JobCreate,
    db=Depends(get_db),
):
    """
    Create a new job
    """
    return create_job(db, job)


@r.put("/jobs/{job_id}", response_model=Job, response_model_exclude_none=True)
async def jobs_edit(
    job_id: int,
    jobs: JobEdit,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Update existing Job
    """
    return edit_job(db, job_id, jobs)


@r.delete(
    "/jobs/{job_id}", response_model=Job, response_model_exclude_none=True
)
async def job_delete(
    job_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Delete existing jobs
    """
    return delete_job(db, job_id)


@er.get("/jobs/steps/{job_id}", response_model=Job)
async def validate_user_job(
    request: Request,
    job_id: int,
    user_id: int,
    mode: str,
    db=Depends(get_db),
):
    """
    Validate user, job and mode and send job steps
    """
    validate_extension_token(request)
    return validate_user_and_job(db, job_id, user_id, mode)


@er.post(
    "/jobs/steps/{job_id}",
    response_model=Job,
    response_model_exclude_none=True,
)
async def save_job_steps(
    request: Request,
    job_id: int,
    jobs: JobEdit,
    db=Depends(get_db),
):
    """
    Save job steps
    """
    validate_extension_token(request)
    return edit_job(db, job_id, jobs)
