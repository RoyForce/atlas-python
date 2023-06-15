from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.db.lessons.models import Lesson
from app.db.core import delete_item
from typing import List, Optional, Any


def create_agility_plan(db: Session, agility_plan: schemas.AgilityPlanCreate):
    db_agility_plan = models.AgilityPlan(
        name=agility_plan.name,
        description=agility_plan.description,
    )
    db.add(db_agility_plan)
    db.commit()
    agility_plan_related_items = [
        {"content": agility_plan.actions, type: "ACTION"},
        {"content": agility_plan.objectives, type: "OBJECTIVE"},
        {"content": agility_plan.leads, type: "LEAD"},
        {"content": agility_plan.sponsors, type: "SPONSOR"},
        {"content": agility_plan.coreteams, type: "CORETEAM"},
        {"content": agility_plan.coaches, type: "COACH"},
        {"content": agility_plan.users, type: "USER"},
        {"content": agility_plan.roles, type: "ROLE"},
    ]

    for related_item in enumerate(agility_plan_related_items):
        relation_count = db.query(models.AgilityPlanRelation).count() + 1
        if (
            related_item["content"] is not None
            and len(related_item["content"]) > 0
        ):
            add_relation_items = [
                models.AgilityPlanRelation(
                    id=relation_count + index,
                    agility_plan_id=db_agility_plan.id,
                    related_id=item,
                    relation_type=related_item["type"],
                )
                for index, item in enumerate(related_item)
            ]
            db.add_all(add_relation_items)
            db.commit()

    db.refresh(db_agility_plan)
    return db_agility_plan


def add_action_to_agility_plan(
    db: Session, action_id: int, agility_plan_id: int
):
    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    db_agility_plan_relation_item = models.AgilityPlanRelation(
        id=relation_count,
        agility_plan_id=agility_plan_id,
        related_id=action_id,
        relation_type="ACTION",
    )
    db.add(db_agility_plan_relation_item)
    db.commit()
    db.refresh(db_agility_plan_relation_item)
    return db_agility_plan_relation_item


def update_agility_plan_by_id(
    db: Session, agility_plan_id: int, agility_plan: schemas.AgilityPlanEdit
):
    update_agility_plan = (
        db.query(models.AgilityPlan)
        .filter(models.AgilityPlan.id == agility_plan_id)
        .update(
            {
                models.AgilityPlan.name: agility_plan.name,
                models.AgilityPlan.description: agility_plan.description,
            }
        )
    )
    remove_relation_items = (
        db.query(models.AgilityPlanRelation)
        .filter(models.AgilityPlanRelation.agility_plan_id == agility_plan_id)
        .delete()
    )
    db.commit()
    agility_plan_related_items = [
        {"content": agility_plan.actions, type: "ACTION"},
        {"content": agility_plan.objectives, type: "OBJECTIVE"},
        {"content": agility_plan.leads, type: "LEAD"},
        {"content": agility_plan.sponsors, type: "SPONSOR"},
        {"content": agility_plan.coreteams, type: "CORETEAM"},
        {"content": agility_plan.coaches, type: "COACH"},
        {"content": agility_plan.users, type: "USER"},
        {"content": agility_plan.roles, type: "ROLE"},
    ]

    for related_item in enumerate(agility_plan_related_items):
        relation_count = db.query(models.AgilityPlanRelation).count() + 1
        if (
            related_item["content"] is not None
            and len(related_item["content"]) > 0
        ):
            add_relation_items = [
                models.AgilityPlanRelation(
                    id=relation_count + index,
                    agility_plan_id=agility_plan_id,
                    related_id=item,
                    relation_type=related_item["type"],
                )
                for index, item in enumerate(related_item)
            ]
            db.add_all(add_relation_items)
            db.commit()

    return update_agility_plan


def add_objective_to_agility_plan(
    db: Session, objective: models.Objective, agility_plan_id: int
):
    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    db_agility_plan_relation_item = models.AgilityPlanRelation(
        id=relation_count,
        agility_plan_id=agility_plan_id,
        related_id=objective.id,
        relation_type="ACTION",
    )
    db.add(db_agility_plan_relation_item)
    db.commit()
    db.refresh(db_agility_plan_relation_item)
    return db_agility_plan_relation_item


def get_agility_plan_by_id(db: Session, agility_plan_id: int):
    try:
        agility_plan = (
            db.query(models.AgilityPlan)
            .filter(models.AgilityPlan.id == agility_plan_id)
            .one()
        )

        return agility_plan
    except:
        return "No result found for query"


def delete_agility_plan_by_id(db: Session, agility_plan_id: int):
    remove_agility_plan_items = (
        db.query(models.AgilityPlan)
        .filter(models.AgilityPlan.id == agility_plan_id)
        .delete()
    )
    db.commit()

    remove_agility_plan_relation_items = (
        db.query(models.AgilityPlanRelation)
        .filter(models.AgilityPlanRelation.agility_plan_id == agility_plan_id)
        .delete()
    )
    db.commit()


def delete_action_to_agility_plan(
    db: Session, action_id: int, agility_plan_id: int
):
    remove_agility_plan_items = (
        db.query(models.AgilityPlanRelation)
        .filter(
            models.AgilityPlanRelation.id == agility_plan_id
            and models.AgilityPlanRelation.related_id == action_id
        )
        .delete()
    )
    db.commit()


def delete_objective_to_agility_plan(
    db: Session, objective_id: int, agility_plan_id: int
):
    remove_agility_plan_items = (
        db.query(models.AgilityPlanRelation)
        .filter(
            models.AgilityPlanRelation.id == agility_plan_id
            and models.AgilityPlanRelation.related_id == objective_id
        )
        .delete()
    )
    db.commit()
