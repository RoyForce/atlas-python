from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.cost_centers import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.cost_centers.schemas import (
    CostCenterCreate,
    CostCenterEdit,
    CostCenterOut,
)

cost_center_router = r = APIRouter()


@r.get(
    "/cost_centers",
    response_model=t.List[CostCenterOut],
)
async def cost_centers_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all cost_centers
    """
    cost_centers = get_lists(db, models.CostCenter, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(cost_centers)}"
    return cost_centers


@r.get(
    "/cost_centers/{cost_center_id}",
    response_model=CostCenterOut,
)
async def cost_center_details(
    cost_center_id: int,
    db=Depends(get_db),
):
    """
    Get any cost_center details
    """
    return get_item(db, models.CostCenter, cost_center_id)


@r.post("/cost_centers", response_model=CostCenterOut)
async def cost_center_create(
    cost_center: CostCenterCreate,
    db=Depends(get_db),
):
    """
    Create a new cost_center
    """
    return create_item(db, models.CostCenter, cost_center)


@r.put("/cost_centers/{cost_center_id}", response_model=CostCenterOut)
async def cost_center_edit(
    cost_center_id: int,
    cost_center: CostCenterEdit,
    db=Depends(get_db),
):
    """
    Update existing cost_center
    """
    return edit_item(db, models.CostCenter, cost_center_id, cost_center)


@r.delete(
    "/cost_centers/{cost_center_id}",
    response_model=CostCenterOut,
)
async def cost_center_delete(
    cost_center_id: int,
    db=Depends(get_db),
):
    """
    Delete existing cost_center
    """
    return delete_item(db, models.CostCenter, cost_center_id)
