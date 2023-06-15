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
    update_agility_plan_by_id,
    delete_agility_plan_by_id,
    add_action_to_agility_plan,
    add_objective_to_agility_plan,
    delete_action_to_agility_plan,
    delete_objective_to_agility_plan,
)

agility_plan_router = r = APIRouter()
AGILITY_PLAN_RELATION_TYPES = [
    "ACTION",
    "OBJECTIVE",
    "LEAD",
    "SPONSOR",
    "CORETEAM",
    "COACH",
    "USER",
    "ROLE",
]


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
    related_ids = dict()
    for agility_plan in filtered_agility_plans:
        for type in AGILITY_PLAN_RELATION_TYPES:
            relations = (
                db.query(models.AgilityPlanRelation)
                .filter(
                    models.AgilityPlanRelation.relation_type == type
                    and models.AgilityPlanRelation.agility_plan_id
                    == agility_plan.id
                )
                .all()
            )
            related_ids[type] = []
            for relation in relations:
                related_ids[type].append(relation.related_id)
        agility_plan.actions = list(
            filter(
                lambda x: x.id in related_ids["ACTION"], agility_plan.actions
            )
        )
        agility_plan.objectives = list(
            filter(
                lambda x: x.id in related_ids["OBJECTIVE"],
                agility_plan.objectives,
            )
        )
        agility_plan.leads = list(
            filter(lambda x: x.id in related_ids["LEAD"], agility_plan.leads)
        )
        agility_plan.sponsors = list(
            filter(
                lambda x: x.id in related_ids["SPONSOR"], agility_plan.sponsors
            )
        )
        agility_plan.coreteams = list(
            filter(
                lambda x: x.id in related_ids["CORETEAM"],
                agility_plan.coreteams,
            )
        )
        agility_plan.coaches = list(
            filter(lambda x: x.id in related_ids["COACH"], agility_plan.coaches)
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
    Get a specific agility-plan details
    """
    agility_plan = get_agility_plan_by_id(db, agility_plan_id)
    if agility_plan == "No result found for query":
        return
    related_ids = dict()
    for type in AGILITY_PLAN_RELATION_TYPES:
        relations = (
            db.query(models.AgilityPlanRelation)
            .filter(
                models.AgilityPlanRelation.relation_type == type
                and models.AgilityPlanRelation.agility_plan_id
                == agility_plan.id
            )
            .all()
        )
        related_ids[type] = []
        for relation in relations:
            related_ids[type].append(relation.related_id)
    agility_plan.actions = list(
        filter(lambda x: x.id in related_ids["ACTION"], agility_plan.actions)
    )
    agility_plan.objectives = list(
        filter(
            lambda x: x.id in related_ids["OBJECTIVE"],
            agility_plan.objectives,
        )
    )
    agility_plan.leads = list(
        filter(lambda x: x.id in related_ids["LEAD"], agility_plan.leads)
    )
    agility_plan.sponsors = list(
        filter(lambda x: x.id in related_ids["SPONSOR"], agility_plan.sponsors)
    )
    agility_plan.coreteams = list(
        filter(
            lambda x: x.id in related_ids["CORETEAM"],
            agility_plan.coreteams,
        )
    )
    agility_plan.coaches = list(
        filter(lambda x: x.id in related_ids["COACH"], agility_plan.coaches)
    )

    return agility_plan


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


@r.delete(
    "/agility-plans/{agility_plan_id}/remove-action/{action_id}",
)
async def agility_plan_action_create(
    agility_plan_id: int,
    action_id: int,
    db=Depends(get_db),
):
    """
    Delete an action from agility-plan
    """
    return delete_action_to_agility_plan(db, action_id, agility_plan_id)


@r.delete(
    "/agility-plans/{agility_plan_id}/remove-objective/{objective_id}",
)
async def agility_plan_objective_create(
    agility_plan_id: int,
    objective_id: int,
    db=Depends(get_db),
):
    """
    Delete an objective from agility-plan
    """
    return delete_objective_to_agility_plan(db, objective_id, agility_plan_id)


@r.post(
    "/agility-plans/{agility_plan_id}/add-action/{action_id}",
)
async def agility_plan_action_create(
    agility_plan_id: int,
    action_id: int,
    db=Depends(get_db),
):
    """
    Add a new action to agility-plan
    """
    return add_action_to_agility_plan(db, action_id, agility_plan_id)


@r.post(
    "/agility-plans/{agility_plan_id}/add-objective/{objective_id}",
)
async def agility_plan_objective_create(
    agility_plan_id: int,
    objective_id: int,
    db=Depends(get_db),
):
    """
    Add a new objective to agility-plan
    """
    return add_objective_to_agility_plan(db, objective_id, agility_plan_id)


@r.put("/agility-plans/{agility_plan_id}")
async def agility_plan_edit(
    agility_plan_id: int,
    agility_plan: AgilityPlanEdit,
    db=Depends(get_db),
):
    """
    Update existing agility_plan
    """
    return update_agility_plan_by_id(db, agility_plan_id, agility_plan)


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
    return delete_agility_plan_by_id(db, agility_plan_id)
