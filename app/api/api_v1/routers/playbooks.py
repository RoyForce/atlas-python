from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.playbooks import models
from app.db.core import (
    get_lists,
    get_item,
    delete_item,
    create_item,
    edit_item,
)
from app.db.playbooks.schemas import (
    PlaybookEdit,
    PlaybookOut,
    PlaybookListOut,
)
from app.core.auth import get_current_active_user

playbook_router = r = APIRouter()


@r.get(
    "/playbooks",
    response_model=t.List[PlaybookListOut],
)
async def playbooks_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all Playbooks
    """
    playbooks = get_lists(db, models.Playbook, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(playbooks)}"
    return playbooks


@r.get(
    "/playbooks/{playbook_id}",
    response_model=PlaybookOut,
)
async def playbook_details(
    playbook_id: int,
    db=Depends(get_db),
):
    """
    Get any playbook details
    """
    return get_item(db, models.Playbook, playbook_id)


@r.post("/playbooks", response_model=PlaybookOut)
async def playbook_create(
    playbook: PlaybookEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new playbook
    """
    playbook.created_by = current_user.id
    return create_item(db, models.Playbook, playbook)


@r.put(
    "/playbooks/{playbook_id}",
    response_model=PlaybookOut,
    response_model_exclude_none=True,
)
async def playbooks_edit(
    playbook_id: int,
    playbook: PlaybookEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing Playbook
    """
    playbook.updated_by = current_user.id
    return edit_item(db, models.Playbook, playbook_id, playbook)


@r.delete(
    "/playbooks/{playbook_id}",
    response_model=PlaybookOut,
)
async def playbook_delete(
    playbook_id: int,
    db=Depends(get_db),
):
    """
    Delete existing playbooks
    """
    return delete_item(db, models.Playbook, playbook_id)
