from fastapi import APIRouter, Request, Depends, Response
from app.db.session import get_db
import typing as t
from app.db.core import (
    get_lists,
    get_item,
    delete_item,
    create_item,
    edit_item,
)
from app.db.job_snippets.models import JobSnippet
from app.db.job_snippets.schemas import (
    JobSnippetEdit,
    JobSnippetOut,
)
from app.core.auth import get_current_active_user

job_snippet_router = r = APIRouter()


@r.get(
    "/job-snippets",
    response_model=t.List[JobSnippetOut],
)
async def jobs_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all job snippets
    """
    job_snippets = get_lists(db, JobSnippet, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(job_snippets)}"
    return job_snippets


@r.get(
    "/job-snippets/{job_snippet_id}",
    response_model=JobSnippetOut,
)
async def job_details(
    job_snippet_id: int,
    db=Depends(get_db),
):
    """
    Get any job snippet details
    """
    return get_item(db, JobSnippet, job_snippet_id)


@r.post("/job-snippets", response_model=JobSnippetOut)
async def job_create(
    job_snippet: JobSnippetEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new job snippet
    """
    job_snippet.created_by = current_user.id
    return create_item(db, JobSnippet, job_snippet)


@r.put("/job-snippets/{job_snippet_id}", response_model=JobSnippetOut)
async def jobs_edit(
    job_snippet_id: int,
    job: JobSnippetEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing job snippet
    """
    job.updated_by = current_user.id
    return edit_item(db, JobSnippet, job_snippet_id, job)


@r.delete("/job-snippets/{job_snippet_id}", response_model=JobSnippetOut)
async def job_delete(
    job_snippet_id: int,
    db=Depends(get_db),
):
    """
    Delete existing job snippet
    """
    return delete_item(db, JobSnippet, job_snippet_id)
