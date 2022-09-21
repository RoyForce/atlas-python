from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t


from app.db.session import get_db
from app.db.playbooks.crud import (
    get_playbooks,
    get_playbook,
    create_playbook,
    delete_playbook,
    edit_playbook,
)
from app.db.playbooks.schemas import (
    PlaybookCreate,
    PlaybookEdit,
    Playbook,
    PlaybookOut,
)
from app.core.auth import get_current_active_superuser

playbook_router = r = APIRouter()


@r.get(
    "/playbooks",
    response_model=t.List[Playbook],
    response_model_exclude_none=True,
)
async def playbooks_list(
    response: Response,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_superuser),
):
    """
    Get all Playbooks
    """
    playbooks = get_playbooks(db)
    response.headers["Content-Range"] = f"0-9/{len(playbooks)}"
    return playbooks


@r.get(
    "/playbooks/{playbook_id}",
    response_model=Playbook,
    response_model_exclude_none=True,
)
async def playbook_details(
    request: Request,
    playbook_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_superuser),
):
    """
    Get any playbook details
    """
    playbooks = get_playbook(db, playbook_id)
    return playbooks


@r.post(
    "/playbooks", response_model=Playbook, response_model_exclude_none=True
)
async def playbook_create(
    request: Request,
    playbook: PlaybookCreate,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_superuser),
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
    request: Request,
    playbook_id: int,
    playbooks: PlaybookEdit,
    db=Depends(get_db),
    current_playbook=Depends(get_current_active_superuser),
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
    request: Request,
    playbook_id: int,
    db=Depends(get_db),
    current_playbook=Depends(get_current_active_superuser),
):
    """
    Delete existing playbooks
    """
    return delete_playbook(db, playbook_id)
