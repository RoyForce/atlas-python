from app.core.auth import get_current_active_user
from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.screens import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.screens.schemas import (
    ScreenCreate,
    ScreenEdit,
    Screen,
)

screens_router = r = APIRouter()


@r.get(
    "/screens",
    response_model=t.List[Screen],
    response_model_exclude_none=True,
)
async def screens_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get all screens
    """
    screens = get_lists(db, models.Screen, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(screens)}"
    return screens


@r.get(
    "/screens/{screen_id}",
    response_model=Screen,
    response_model_exclude_none=True,
)
async def screens_details(
    screen_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get any screen details
    """
    return get_item(db, models.Screen, screen_id)


@r.post(
    "/screens",
    response_model=Screen,
    response_model_exclude_none=True,
)
async def screens_create(
    screen: ScreenCreate,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Create a new screen
    """
    return create_item(db, models.Screen, screen)


@r.put(
    "/screens/{screen_id}",
    response_model=Screen,
    response_model_exclude_none=True,
)
async def screens_edit(
    screen_id: int,
    screen: ScreenEdit,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Update existing screen
    """
    return edit_item(db, models.Screen, screen_id, screen)


@r.delete(
    "/screens/{screen_id}",
    response_model=Screen,
    response_model_exclude_none=True,
)
async def screens_delete(
    screen_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Delete existing screen
    """
    return delete_item(db, models.Screen, screen_id)
