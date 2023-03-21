from fastapi import APIRouter, Depends, Response, Request
import typing as t


from app.db.session import get_db
from app.db.playbooks import models
from app.db.core import get_lists, get_item, delete_item

from app.db.playbooks.crud import (
    create_playbook,
    edit_playbook,
)
from app.db.playbooks.schemas import (
    PlaybookCreate,
    PlaybookEdit,
    Playbook,
)

playbook_router = r = APIRouter()


@r.get(
    "/playbooks",
    response_model=t.List[Playbook],
    response_model_exclude_none=True,
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
    response_model=Playbook,
    response_model_exclude_none=True,
)
async def playbook_details(
    playbook_id: int,
    db=Depends(get_db),
):
    """
    Get any playbook details
    """
    return get_item(db, models.Playbook, playbook_id)


@r.post(
    "/playbooks", response_model=Playbook, response_model_exclude_none=True
)
async def playbook_create(
    playbook: PlaybookCreate,
    db=Depends(get_db),
):
    """
    Create a new playbook
    """
    return create_playbook(db, playbook)


@r.put(
    "/playbooks/{playbook_id}",
    response_model=Playbook,
    response_model_exclude_none=True,
)
async def playbooks_edit(
    playbook_id: int,
    playbooks: PlaybookEdit,
    db=Depends(get_db),
):
    """
    Update existing Playbook
    """
    return edit_playbook(db, playbook_id, playbooks)


@r.delete(
    "/playbooks/{playbook_id}",
    response_model=Playbook,
    response_model_exclude_none=True,
)
async def playbook_delete(
    playbook_id: int,
    db=Depends(get_db),
):
    """
    Delete existing playbooks
    """
    return delete_item(db, models.Playbook, playbook_id)
