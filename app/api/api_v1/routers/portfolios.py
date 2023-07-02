from fastapi import APIRouter, Request, Depends, Response, HTTPException
import typing as t

from app.db.session import get_db
from app.db.portfolios import models
from app.db.teams import models as TeamModel
from app.db.programs import models as ProgramModel
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    edit_item,
    delete_item,
    get_items_by_key,
)
from app.db.portfolios.schemas import (
    PortfolioCreate,
    PortfolioEdit,
    PortfolioOut,
)
from app.core.auth import get_current_active_user


portfolio_router = r = APIRouter()


@r.get(
    "/portfolios",
    response_model=t.List[PortfolioOut],
)
async def portfolios_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all portfolios
    """
    portfolios = get_lists(db, models.Portfolio, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(portfolios)}"
    return portfolios


@r.get(
    "/portfolios/{portfolio_id}",
    response_model=PortfolioOut,
)
async def portfolio_details(
    portfolio_id: int,
    db=Depends(get_db),
):
    """
    Get any portfolio details
    """
    return get_item(db, models.Portfolio, portfolio_id)


@r.post("/portfolios", response_model=PortfolioOut)
async def portfolio_create(
    portfolio: PortfolioCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new portfolio
    """
    team = TeamModel.Team()
    team = TeamModel.Team(
        name=portfolio.name + " Team",
        description=portfolio.description,
        created_by=current_user.id,
        type=5,
    )
    db.add(team)
    db.commit()
    portfolio.team_id = team.id
    portfolio.created_by = current_user.id
    return create_item(db, models.Portfolio, portfolio)


@r.put("/portfolios/{portfolio_id}", response_model=PortfolioOut)
async def portfolio_edit(
    portfolio_id: int,
    portfolio: PortfolioEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing portfolio
    """
    portfolio.updated_by = current_user.id
    return edit_item(db, models.Portfolio, portfolio_id, portfolio)


@r.delete(
    "/portfolios/{portfolio_id}",
    response_model=PortfolioOut,
)
async def portfolio_delete(
    portfolio_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Delete existing portfolio
    """
    item = get_item(db, models.Portfolio, portfolio_id)
    if (
        "source_id" in item.dict()
        and item.source_id is not None
        and item.is_deleted == False
    ):
        raise HTTPException(
            status_code=403, detail="Can not delete external item"
        )
    else:
        if item.team_id is not None:
            delete_item(db, TeamModel.Team, item.team_id)
        filters = ProgramModel.Program.portfolio_id == item.id
        programs = get_items_by_key(db, ProgramModel.Program, filters)
        for program in programs:
            program.portfolio_id = None
            program.updated_by = current_user.id
            db.add(program)
            db.commit()
            db.refresh(program)
    db.delete(item)
    db.commit()
    return item
