from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t


from app.db.session import get_db
from app.db.use_cases.crud import (
    get_use_cases,
    get_use_case,
    create_use_case,
    delete_use_case,
    edit_use_case,
)
from app.db.use_cases.schemas import (
    UseCaseCreate,
    UseCaseEdit,
    UseCase,
    UseCaseOut,
)
from app.core.auth import get_current_active_superuser

use_case_router = r = APIRouter()


@r.get(
    "/use-cases",
    response_model=t.List[UseCase],
    response_model_exclude_none=True,
)
async def use_cases_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all UseCases
    """
    use_cases = get_use_cases(db)
    response.headers["Content-Range"] = f"0-9/{len(use_cases)}"
    return use_cases


@r.get(
    "/use-cases/{use_case_id}",
    response_model=UseCase,
    response_model_exclude_none=True,
)
async def use_case_details(
    use_case_id: int,
    db=Depends(get_db),
):
    """
    Get any use_case details
    """
    use_cases = get_use_case(db, use_case_id)
    return use_cases


@r.post("/use-cases", response_model=UseCase, response_model_exclude_none=True)
async def use_case_create(
    use_case: UseCaseCreate,
    db=Depends(get_db),
):
    """
    Create a new use_case
    """
    return create_use_case(db, use_case)


@r.put(
    "/use-cases/{use_case_id}",
    response_model=UseCase,
    response_model_exclude_none=True,
)
async def use_cases_edit(
    use_case_id: int,
    use_cases: UseCaseEdit,
    db=Depends(get_db),
):
    """
    Update existing UseCase
    """
    return edit_use_case(db, use_case_id, use_cases)


@r.delete(
    "/use-cases/{use_case_id}",
    response_model=UseCase,
    response_model_exclude_none=True,
)
async def use_case_delete(
    use_case_id: int,
    db=Depends(get_db),
):
    """
    Delete existing use_cases
    """
    return delete_use_case(db, use_case_id)
