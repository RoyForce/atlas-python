from fastapi import APIRouter, Depends, Response, Request, HTTPException
import typing as t
from app.db.users import models

from app.db.session import get_db
from app.db.measurements.models import Measurement
from app.db.objectives.models import Objective
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.measurements.schemas import (
    MeasurementEdit,
    MeasurementOut,
)
from app.db.enums import MetricsType

from app.core.auth import get_current_active_user

measurement_router = r = APIRouter()


@r.get(
    "/measurements/{objective_id}",
)
async def measurement_list(
    objective_id: int,
    db=Depends(get_db),
):
    """
    Get all measurement
    """
    items = (
        db.query(Measurement)
        .filter(Measurement.objective_id == objective_id)
        .all()
    )
    for measurement in items:
        user = (
            db.query(models.User)
            .filter(models.User.id == measurement.created_by)
            .one()
        )
        measurement.created_by = user.first_name
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items


@r.post(
    "/measurements",
)
async def measurement_create(
    request: Request,
    measurement: MeasurementEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new measurement
    """
    measurement.created_by = current_user.id
    objective = (
        db.query(Objective)
        .filter(Objective.id == measurement.objective_id)
        .one()
    )
    if objective.metrics_type == MetricsType.PERCENTAGE:
        if not 0 <= measurement.value <= 100:
            raise HTTPException(status_code=406, detail="Invalid Value")
    else:
        if not 0 <= measurement.value:
            raise HTTPException(status_code=406, detail="Invalid Value")
    result = create_item(db, Measurement, measurement)
    result.stwert = current_user.first_name
    return result


@r.put(
    "/measurements/{measurement_id}",
    response_model=MeasurementOut,
)
async def measurement_edit(
    measurement_id: int,
    measurement: MeasurementEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing measurement
    """
    measurement.updated_by = current_user.id
    return edit_item(db, Measurement, measurement_id, measurement)


@r.delete(
    "/measurements/{measurement_id}",
    response_model=MeasurementOut,
)
async def measurement_delete(
    measurement_id: int,
    db=Depends(get_db),
):
    """
    Delete existing measurement
    """
    return delete_item(db, Measurement, measurement_id)
