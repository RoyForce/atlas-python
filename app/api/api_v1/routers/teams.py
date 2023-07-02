from fastapi import APIRouter, Request, Depends, Response, HTTPException
import typing as t

from app.db.session import get_db
from app.db.teams import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.teams.schemas import (
    TeamCreate,
    TeamEdit,
    TeamOut,
)

from app.db.programs import models as ProgramModel
from app.db.portfolios import models as portfolioModel
from app.core.auth import get_current_active_user

team_router = r = APIRouter()


@r.get(
    "/teams",
    response_model=t.List[TeamOut],
)
async def teams_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all teams
    """
    teams = get_lists(db, models.Team, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(teams)}"
    return teams


@r.get(
    "/teams/{team_id}",
    response_model=TeamOut,
)
async def team_details(
    team_id: int,
    db=Depends(get_db),
):
    """
    Get any team details
    """
    return get_item(db, models.Team, team_id)


@r.post("/teams", response_model=TeamOut)
async def team_create(
    team: TeamCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new team
    """
    team.created_by = current_user.id
    return create_item(db, models.Team, team)


@r.put("/teams/{team_id}", response_model=TeamOut)
async def team_edit(
    team_id: int,
    team: TeamEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing team
    """
    team.updated_by = current_user.id
    return edit_item(db, models.Team, team_id, team)


@r.delete(
    "/teams/{team_id}",
    response_model=TeamOut,
)
async def team_delete(
    team_id: int,
    db=Depends(get_db),
):
    """
    Delete existing team
    """
    item = get_item(db, models.Team, team_id)
    if (
        "source_id" in item.dict()
        and item.source_id is not None
        and item.is_deleted == False
    ):
        raise HTTPException(
            status_code=403, detail="Can not delete external item"
        )
    if item.type == 2 and item.program_id is not None:
        raise HTTPException(
            status_code=403,
            detail="Program team associated with some Program can only be deleted when removing the Program from Administration.",
        )
    if item.type == 5:
        raise HTTPException(
            status_code=403,
            detail="Portfolio team associated with some Portfolio can only be deleted when removing the Portfolio from Administration.",
        )
    item.program_id = None
    db.add(item)
    db.commit()
    db.delete(item)
    db.commit()
    return item
