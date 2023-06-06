from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.objectives.models import Objective
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.objectives.schemas import (
    ObjectiveEdit,
    ObjectiveOut,
)

from app.core.auth import get_current_active_user

objective_router = r = APIRouter()


@r.get(
    "/objectives",
    response_model=t.List[ObjectiveOut],
)
async def objective_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all objective
    """
    objectives = get_lists(db, Objective, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(objectives)}"
    return objectives


@r.get(
    "/objectives/{objective_id}",
    response_model=ObjectiveOut,
)
async def objective_details(
    objective_id: int,
    db=Depends(get_db),
):
    """
    Get any objective details
    """
    return get_item(db, Objective, objective_id)


@r.post(
    "/objectives",
    response_model=ObjectiveOut,
)
async def objective_create(
    request: Request,
    objective: ObjectiveEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new objective
    """
    objective.created_by = current_user.id
    return create_item(db, Objective, objective)


@r.put(
    "/objectives/{objective_id}",
    response_model=ObjectiveOut,
)
async def objective_edit(
    objective_id: int,
    objective: ObjectiveEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing objective
    """
    objective.updated_by = current_user.id
    return edit_item(db, Objective, objective_id, objective)


@r.delete(
    "/objectives/{objective_id}",
    response_model=ObjectiveOut,
)
async def objective_delete(
    objective_id: int,
    db=Depends(get_db),
):
    """
    Delete existing objective
    """
    return delete_item(db, Objective, objective_id)
