from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.external_data.external_api import (
    fetch_data_api,
    validate_external_api_token,
)

external_api_router = r = APIRouter()


@r.get(
    "/fetch-external-data",
    response_model="",
    response_model_exclude_none=True,
)
async def fetch_data(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    # validate_external_api_token(request)
    return fetch_data_api(db)
