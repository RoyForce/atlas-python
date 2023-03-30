from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.application_types import models
from app.db.core import get_lists, get_item

from app.db.application_types.schemas import (
    ApplicationTypeOut,
)

application_types_router = r = APIRouter()


@r.get(
    "/application-types",
    response_model=t.List[ApplicationTypeOut],
    response_model_exclude_none=True,
)
async def applicationTypes_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all applicationTypes
    """
    application_types = get_lists(
        db, models.ApplicationType, request.query_params
    )
    response.headers["Content-Range"] = f"0-9/{len(application_types)}"
    return application_types


@r.get(
    "/application-types/{application_types_id}",
    response_model=ApplicationTypeOut,
    response_model_exclude_none=True,
)
async def screens_details(
    application_types_id: int,
    db=Depends(get_db),
):
    """
    Get any application types
    """
    return get_item(db, models.ApplicationType, application_types_id)
