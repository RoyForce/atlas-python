from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.use_cases import models
from app.db.core import (
    get_lists,
    get_item,
    delete_item,
    create_item,
    edit_item,
)
from app.db.use_cases.schemas import (
    UseCaseCreate,
    UseCaseEdit,
    UseCaseOut,
)

use_case_router = r = APIRouter()


@r.get(
    "/use-cases",
    response_model=t.List[UseCaseOut],
)
async def use_cases_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all UseCases
    """
    use_cases = get_lists(db, models.UseCase, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(use_cases)}"
    return use_cases


@r.get(
    "/use-cases/{use_case_id}",
    response_model=UseCaseOut,
)
async def use_case_details(
    use_case_id: int,
    db=Depends(get_db),
):
    """
    Get any use_case details
    """
    return get_item(db, models.UseCase, use_case_id)


@r.post("/use-cases", response_model=UseCaseOut)
async def use_case_create(
    use_case: UseCaseCreate,
    db=Depends(get_db),
):
    """
    Create a new use_case
    """
    return create_item(db, models.UseCase, use_case)


@r.put(
    "/use-cases/{use_case_id}",
    response_model=UseCaseOut,
)
async def use_cases_edit(
    use_case_id: int,
    use_case: UseCaseEdit,
    db=Depends(get_db),
):
    """
    Update existing UseCase
    """
    return edit_item(db, models.UseCase, use_case_id, use_case)


@r.delete(
    "/use-cases/{use_case_id}",
    response_model=UseCaseOut,
)
async def use_case_delete(
    use_case_id: int,
    db=Depends(get_db),
):
    """
    Delete existing use_cases
    """
    return delete_item(db, models.UseCase, use_case_id)
