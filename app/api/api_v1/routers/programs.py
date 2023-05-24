from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.programs import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.programs.schemas import (
    ProgramCreate,
    ProgramEdit,
    ProgramOut,
)

program_router = r = APIRouter()


@r.get(
    "/programs",
    response_model=t.List[ProgramOut],
)
async def programs_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all programs
    """
    programs = get_lists(db, models.Program, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(programs)}"
    return programs


@r.get(
    "/programs/{program_id}",
    response_model=ProgramOut,
)
async def program_details(
    program_id: int,
    db=Depends(get_db),
):
    """
    Get any program details
    """
    return get_item(db, models.Program, program_id)


@r.post("/programs", response_model=ProgramOut)
async def program_create(
    program: ProgramCreate,
    db=Depends(get_db),
):
    """
    Create a new program
    """
    return create_item(db, models.Program, program)


@r.put("/programs/{program_id}", response_model=ProgramOut)
async def program_edit(
    program_id: int,
    program: ProgramEdit,
    db=Depends(get_db),
):
    """
    Update existing program
    """
    return edit_item(db, models.Program, program_id, program)


@r.delete(
    "/programs/{program_id}",
    response_model=ProgramOut,
)
async def program_delete(
    program_id: int,
    db=Depends(get_db),
):
    """
    Delete existing program
    """
    return delete_item(db, models.Program, program_id)
