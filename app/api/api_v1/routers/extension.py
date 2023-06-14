from fastapi import APIRouter, Request, Depends
from app.db.jobs.models import Job
from app.db.job_snippets.models import JobSnippet
from app.db.session import get_db
from app.db.jobs.crud import (
    validate_user_and_job,
)
from app.db.jobs.schemas import (
    JobEdit,
    JobOut,
)
from app.db.job_snippets.schemas import (
    JobSnippetOut,
)
from app.db.core import (
    get_lists,
    edit_item,
)
from app.core.auth import get_current_active_user

extension_router = er = APIRouter()


@er.get("/jobs/{job_id}", response_model=JobOut)
async def validate_user_job(
    job_id: int,
    user_id: int,
    mode: str,
    db=Depends(get_db),
):
    """
    Validate user, job and mode and send job steps
    """
    return validate_user_and_job(db, job_id, user_id, mode)


@er.post(
    "/jobs/{job_id}",
    response_model=JobOut,
    response_model_exclude_none=True,
)
async def save_job_steps(
    job_id: int,
    job: JobEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Save job steps
    """
    job.updated_by = current_user.id
    return edit_item(db, Job, job_id, job)


@er.get("/job-snippets/{job_snippet_id}", response_model=JobSnippetOut)
async def job_snippet_list(
    job_id: int,
    db=Depends(get_db),
):
    """
    Get job snippets
    """
    return get_lists(db, JobSnippet, job_id)
