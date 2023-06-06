from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.dimensions.models import Dimension
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.dimensions.schemas import (
    DimensionEdit,
    DimensionOut,
)

from app.core.auth import get_current_active_user

dimension_router = r = APIRouter()


@r.get(
    "/dimensions",
    response_model=t.List[DimensionOut],
)
async def dimension_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all dimension
    """
    dimensions = get_lists(db, Dimension, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(dimensions)}"
    return dimensions


@r.get(
    "/dimensions/{dimension_id}",
    response_model=DimensionOut,
)
async def dimension_details(
    dimension_id: int,
    db=Depends(get_db),
):
    """
    Get any dimension details
    """
    return get_item(db, Dimension, dimension_id)


@r.post(
    "/dimensions",
    response_model=DimensionOut,
)
async def dimension_create(
    dimension: DimensionEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new dimension
    """

    dimension.created_by = current_user.id
    return create_item(db, Dimension, dimension)


@r.put(
    "/dimensions/{dimension_id}",
    response_model=DimensionOut,
)
async def dimension_edit(
    dimension_id: int,
    dimension: DimensionEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing dimension
    """
    dimension.updated_by = current_user.id
    return edit_item(db, Dimension, dimension_id, dimension)


@r.delete(
    "/dimensions/{dimension_id}",
    response_model=DimensionOut,
)
async def dimension_delete(
    dimension_id: int,
    db=Depends(get_db),
):
    """
    Delete existing dimension
    """
    return delete_item(db, Dimension, dimension_id)
