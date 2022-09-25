from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t


from app.db.session import get_db
from app.db.jobs.crud import (
    get_jobs,
    get_job,
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
from app.core.auth import get_current_active_superuser

jobs_router = r = APIRouter()
extension_router = er = APIRouter()


@r.get(
    "/jobs",
    response_model=t.List[Job],
    response_model_exclude_none=True,
)
async def jobs_list(
    response: Response,
    db=Depends(get_db),
    current_jobs=Depends(get_current_active_superuser),
):
    """
    Get all Jobs
    """
    jobs = get_jobs(db)
    response.headers["Content-Range"] = f"0-9/{len(jobs)}"
    return jobs


@r.get(
    "/jobs/{job_id}",
    response_model=Job,
    response_model_exclude_none=True,
)
async def job_details(
    request: Request,
    job_id: int,
    db=Depends(get_db),
    current_jobs=Depends(get_current_active_superuser),
):
    """
    Get any job details
    """
    jobs = get_job(db, job_id)
    return jobs


@r.post("/jobs", response_model=Job, response_model_exclude_none=True)
async def job_create(
    request: Request,
    job: JobCreate,
    db=Depends(get_db),
    current_jobs=Depends(get_current_active_superuser),
):
    """
    Create a new job
    """
    return create_job(db, job)


@r.put("/jobs/{job_id}", response_model=Job, response_model_exclude_none=True)
async def jobs_edit(
    request: Request,
    job_id: int,
    jobs: JobEdit,
    db=Depends(get_db),
    current_job=Depends(get_current_active_superuser),
):
    """
    Update existing Job
    """
    return edit_job(db, job_id, jobs)


@r.delete(
    "/jobs/{job_id}", response_model=Job, response_model_exclude_none=True
)
async def job_delete(
    request: Request,
    job_id: int,
    db=Depends(get_db),
    current_job=Depends(get_current_active_superuser),
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
