from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.screen_objects.models import ScreenObject
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.screen_objects.schemas import (
    ScreenObjectEdit,
    ScreenObjectOut,
)

screen_objects_router = r = APIRouter()


@r.get(
    "/screen-objects",
    response_model=t.List[ScreenObjectOut],
)
async def screen_objects_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all screen objects
    """
    screen_objects = get_lists(db, ScreenObject, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(screen_objects)}"
    return screen_objects


@r.get(
    "/screen-objects/{screen_object_id}",
    response_model=ScreenObjectOut,
)
async def screens_objects_details(
    screen_object_id: int,
    db=Depends(get_db),
):
    """
    Get any screen object details
    """
    return get_item(db, ScreenObject, screen_object_id)


@r.post(
    "/screen-objects",
    response_model=ScreenObjectOut,
)
async def screen_object_create(
    screen_object: ScreenObjectEdit,
    db=Depends(get_db),
):
    """
    Create a new screen object
    """
    return create_item(db, ScreenObject, screen_object)


@r.put(
    "/screen-objects/{screen_object_id}",
    response_model=ScreenObjectOut,
)
async def screens_edit(
    screen_object_id: int,
    screen_object: ScreenObjectEdit,
    db=Depends(get_db),
):
    """
    Update existing screen object
    """
    return edit_item(db, ScreenObject, screen_object_id, screen_object)


@r.delete(
    "/screen-objects/{screen_object_id}",
    response_model=ScreenObjectOut,
)
async def screens_delete(
    screen_object_id: int,
    db=Depends(get_db),
):
    """
    Delete existing screen object
    """
    return delete_item(db, ScreenObject, screen_object_id)
