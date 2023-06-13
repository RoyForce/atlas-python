from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.actions import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.actions.schemas import (
    ActionCreate,
    ActionEdit,
    ActionOut,
    ActionListOut,
)

action_router = r = APIRouter()


@r.get(
    "/actions",
    response_model=t.List[ActionListOut],
)
async def actions_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all actions
    """
    actions = get_lists(db, models.Action, request.query_params)
    filtered_actions = [action for action in actions]
    response.headers["Content-Range"] = f"0-9/{len(filtered_actions)}"
    return filtered_actions


@r.get(
    "/actions/{action_id}",
    response_model=ActionOut,
)
async def action_details(
    action_id: int,
    db=Depends(get_db),
):
    """
    Get any action details
    """
    return get_item(db, models.Action, action_id)


@r.post("/actions", response_model=ActionOut)
async def action_create(
    action: ActionCreate,
    db=Depends(get_db),
):
    """
    Create a new action
    """
    return create_item(db, models.Action, action)


@r.put("/actions/{action_id}", response_model=ActionOut)
async def action_edit(
    action_id: int,
    action: ActionEdit,
    db=Depends(get_db),
):
    """
    Update existing action
    """
    return edit_item(db, models.Action, action_id, action)


@r.delete(
    "/actions/{action_id}",
    response_model=ActionOut,
)
async def action_delete(
    action_id: int,
    db=Depends(get_db),
):
    """
    Delete existing action
    """
    return delete_item(db, models.Action, action_id)
