from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.results.models import Result
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.results.schemas import (
    ResultEdit,
    ResultOut,
)

from app.core.auth import get_current_active_user

result_router = r = APIRouter()


@r.post(
    "/results",
    response_model=ResultOut,
)
async def result_create(
    request: Request,
    result: ResultEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new result
    """
    result.created_by = current_user.id
    return create_item(db, Result, result)


@r.put(
    "/results/{result_id}",
    response_model=ResultOut,
)
async def result_edit(
    result_id: int,
    result: ResultEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing result
    """
    result.updated_by = current_user.id
    return edit_item(db, Result, result_id, result)


@r.delete(
    "/results/{result_id}",
    response_model=ResultOut,
)
async def result_delete(
    result_id: int,
    db=Depends(get_db),
):
    """
    Delete existing result
    """
    return delete_item(db, Result, result_id)
