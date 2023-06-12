from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.programs import models
from app.db.teams import models as TeamModel
from app.db.portfolios import models as portfolioModel
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
    soft_delete_item,
)
from app.db.programs.schemas import (
    ProgramEdit,
    ProgramOut,
)
from app.core.auth import get_current_active_user

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
    program: ProgramEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new program
    """
    db_team = TeamModel.Team(
        name=program.name + " Team",
        description=program.description,
        type=2,
        created_by=current_user.id,
    )
    db.add(db_team)
    db.commit()

    program.team_id = db_team.id
    program.created_by = current_user.id
    db_program = create_item(db, models.Program, program)

    up_team_data = dict(exclude_unset=True)
    up_team_data["program_id"] = (db_program.id,)
    for key, value in up_team_data.items():
        setattr(db_team, key, value)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    db_portfolio = get_item(db, portfolioModel.Portfolio, program.portfolio_id)
    db_port_team = get_item(db, TeamModel.Team, db_portfolio.team_id)
    up_team_data = dict(exclude_unset=True)
    up_team_data["program_id"] = (db_program.id,)
    for key, value in up_team_data.items():
        setattr(db_port_team, key, value)
    db.add(db_port_team)
    db.commit()
    db.refresh(db_port_team)
    return db_program


@r.put("/programs/{program_id}", response_model=ProgramOut)
async def program_edit(
    program_id: int,
    program: ProgramEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing program
    """
    program.updated_by = current_user.id
    db_program = edit_item(db, models.Program, program_id, program)
    if db_program.portfolio_id is not None:
        db_portfolio = get_item(
            db, portfolioModel.Portfolio, program.portfolio_id
        )
        if db_portfolio.team_id is not None:
            db_port_team = get_item(db, TeamModel.Team, db_portfolio.team_id)
            db_port_team.program_id = db_program.id
            db_port_team.updated_by = current_user.id
            db.add(db_port_team)
            db.commit()
            db.refresh(db_port_team)
    return db_program


@r.delete(
    "/programs/{program_id}",
    response_model=ProgramOut,
)
async def program_delete(
    program_id: int,
    db=Depends(get_db),
):
    """
    Soft delete existing program
    """
    return soft_delete_item(db, models.Program, program_id)
