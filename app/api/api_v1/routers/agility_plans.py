from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.agility_plans import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.agility_plans.schemas import (
    AgilityPlanCreate,
    AgilityPlanEdit,
    AgilityPlanOut,
    AgilityPlanListOut,
    AgilityPlanBase,
    AgilityPlan,
)
from app.db.agility_plans.crud import (
    create_agility_plan,
    get_agility_plan_by_id,
)

agility_plan_router = r = APIRouter()


@r.get(
    "/agility-plans",
    response_model=t.List[AgilityPlanListOut],
)
async def agility_plans_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all agility-plans
    """
    agility_plans = get_lists(db, models.AgilityPlan, request.query_params)
    filtered_agility_plans = [agility_plan for agility_plan in agility_plans]

    for agility_plan in filtered_agility_plans:
        relations = (
            db.query(models.AgilityPlanRelation)
            .filter(
                models.AgilityPlanRelation.relation_type == "ACTION"
                and models.AgilityPlanRelation.agility_plan_id
                == agility_plan.id
            )
            .all()
        )
        related_ids = []
        for relation in relations:
            related_ids.append(relation.related_id)
        agility_plan.actions = list(
            filter(lambda x: x.id in related_ids, agility_plan.actions)
        )

    for agility_plan in filtered_agility_plans:
        relations = (
            db.query(models.AgilityPlanRelation)
            .filter(
                models.AgilityPlanRelation.relation_type == "OBJECTIVE"
                and models.AgilityPlanRelation.agility_plan_id
                == agility_plan.id
            )
            .all()
        )
        related_ids = []
        for relation in relations:
            related_ids.append(relation.related_id)
        agility_plan.objectives = list(
            filter(lambda x: x.id in related_ids, agility_plan.objectives)
        )

    response.headers["Content-Range"] = f"0-9/{len(filtered_agility_plans)}"
    return filtered_agility_plans


@r.get(
    "/agility-plans/{agility_plan_id}",
)
async def agility_plan_details(
    agility_plan_id: int,
    db=Depends(get_db),
):
    """
    Get any agility-plan details
    """
    return get_agility_plan_by_id(db, agility_plan_id)


@r.post(
    "/agility-plans",
)
async def agility_plan_create(
    agility_plan: AgilityPlanCreate,
    db=Depends(get_db),
):
    """
    Create a new agility-plan
    """
    return create_agility_plan(db, agility_plan)


@r.put("/agility-plans/{agility_plan_id}", response_model=AgilityPlanOut)
async def agility_plan_edit(
    agility_plan_id: int,
    agility_plan: AgilityPlanEdit,
    db=Depends(get_db),
):
    """
    Update existing agility_plan
    """
    return edit_item(db, models.AgilityPlan, agility_plan_id, agility_plan)


@r.delete(
    "/agility-plans/{agility_plan_id}",
    response_model=AgilityPlanOut,
)
async def agility_plan_delete(
    agility_plan_id: int,
    db=Depends(get_db),
):
    """
    Delete existing agility-plan
    """
    return delete_item(db, models.AgilityPlan, agility_plan_id)
