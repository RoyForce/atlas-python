from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.jobs import models
from app.db.session import get_db
from app.db.jobs.crud import (
    format_job_steps,
    delete_job_mapping,
    validate_extension_token,
    validate_user_and_job,
)
from app.db.jobs.schemas import (
    JobEdit,
    JobOut,
)
from app.db.core import (
    get_lists,
    get_item,
    delete_item,
    create_item,
    edit_item,
)

jobs_router = r = APIRouter()
extension_router = er = APIRouter()


@r.get(
    "/jobs",
    response_model=t.List[JobOut],
)
async def jobs_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all Jobs
    """
    jobs = get_lists(db, models.Job, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(jobs)}"
    return jobs


@r.get(
    "/jobs/{job_id}",
    response_model=JobOut,
)
async def job_details(
    job_id: int,
    db=Depends(get_db),
):
    """
    Get any job details
    """
    return get_item(db, models.Job, job_id)


@r.post("/jobs", response_model=JobOut)
async def job_create(
    job: JobEdit,
    db=Depends(get_db),
):
    """
    Create a new job
    """
    return create_item(db, models.Job, job)


@r.put("/jobs/{job_id}", response_model=JobOut)
async def jobs_edit(
    job_id: int,
    job: JobEdit,
    db=Depends(get_db),
):
    """
    Update existing Job
    """

    job = format_job_steps(job)
    return edit_item(db, models.Job, job_id, job)


@r.delete("/jobs/{job_id}", response_model=JobOut)
async def job_delete(
    job_id: int,
    db=Depends(get_db),
):
    """
    Delete existing jobs
    """
    delete_job_mapping(db, job_id)
    return delete_item(db, models.Job, job_id)


@er.get("/jobs/steps/{job_id}", response_model=JobOut)
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
    response_model=JobOut,
    response_model_exclude_none=True,
)
async def save_job_steps(
    request: Request,
    job_id: int,
    job: JobEdit,
    db=Depends(get_db),
):
    """
    Save job steps
    """
    validate_extension_token(request)
    job = format_job_steps(job)
    return edit_item(db, models.Job, job_id, job)
