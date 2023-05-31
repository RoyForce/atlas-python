from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.portfolios import models
from app.db.teams import models as TeamModel
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
    soft_delete_item,
)
from app.db.portfolios.schemas import (
    PortfolioCreate,
    PortfolioEdit,
    PortfolioOut,
)


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
):
    """
    Create a new portfolio
    """
    team = TeamModel.Team()
    team = TeamModel.Team(
        name=portfolio.name + " Team",
        description=portfolio.description,
        type=5,
    )
    db.add(team)
    db.commit()
    portfolio.team_id = team.id
    return create_item(db, models.Portfolio, portfolio)


@r.put("/portfolios/{portfolio_id}", response_model=PortfolioOut)
async def portfolio_edit(
    portfolio_id: int,
    portfolio: PortfolioEdit,
    db=Depends(get_db),
):
    """
    Update existing portfolio
    """
    return edit_item(db, models.Portfolio, portfolio_id, portfolio)


@r.delete(
    "/portfolios/{portfolio_id}",
    response_model=PortfolioOut,
)
async def portfolio_delete(
    portfolio_id: int,
    db=Depends(get_db),
):
    """
    Delete existing portfolio
    """
    return soft_delete_item(db, models.Portfolio, portfolio_id)
