from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.assessments.models import Assessment
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.assessments.schemas import (
    AssessmentEdit,
    AssessmentOut,
)

from app.core.auth import get_current_active_user

assessment_router = r = APIRouter()


@r.get(
    "/assessments",
    response_model=t.List[AssessmentOut],
)
async def assessment_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all assessment
    """
    assessments = get_lists(db, Assessment, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(assessments)}"
    return assessments


@r.get(
    "/assessments/{assessment_id}",
    response_model=AssessmentOut,
)
async def assessment_details(
    assessment_id: int,
    db=Depends(get_db),
):
    """
    Get any assessment details
    """
    return get_item(db, Assessment, assessment_id)


@r.post(
    "/assessments",
    response_model=AssessmentOut,
)
async def assessment_create(
    request: Request,
    assessment: AssessmentEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new assessment
    """
    assessment.created_by = current_user.id
    return create_item(db, Assessment, assessment)


@r.put(
    "/assessments/{assessment_id}",
    response_model=AssessmentOut,
)
async def assessment_edit(
    assessment_id: int,
    assessment: AssessmentEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing assessment
    """
    assessment.updated_by = current_user.id
    return edit_item(db, Assessment, assessment_id, assessment)


@r.delete(
    "/assessments/{assessment_id}",
    response_model=AssessmentOut,
)
async def assessment_delete(
    assessment_id: int,
    db=Depends(get_db),
):
    """
    Delete existing assessment
    """
    return delete_item(db, Assessment, assessment_id)
