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
    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.actions is not None and len(agility_plan.actions) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=item,
                relation_type="ACTION",
            )
            for index, item in enumerate(agility_plan.actions)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.objectives is not None and len(agility_plan.objectives) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="OBJECTIVE",
            )
            for index, items in enumerate(agility_plan.objectives)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.leads is not None and len(agility_plan.leads) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="LEAD",
            )
            for index, items in enumerate(agility_plan.leads)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.sponsors is not None and len(agility_plan.sponsors) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="SPONSOR",
            )
            for index, items in enumerate(agility_plan.sponsors)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.coreteams is not None and len(agility_plan.coreteams) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="CORETEAM",
            )
            for index, items in enumerate(agility_plan.coreteams)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.coaches is not None and len(agility_plan.coaches) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="COACH",
            )
            for index, items in enumerate(agility_plan.coaches)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.users is not None and len(agility_plan.users) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="USER",
            )
            for index, items in enumerate(agility_plan.users)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.roles is not None and len(agility_plan.roles) > 0:
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items,
                relation_type="ROLE",
            )
            for index, items in enumerate(agility_plan.roles)
        ]
        db.add_all(db_agility_plan_relation_item)
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
    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.actions is not None and len(agility_plan.actions) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="ACTION",
            )
            for index, item in enumerate(agility_plan.actions)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.objectives is not None and len(agility_plan.objectives) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="OBJECTIVE",
            )
            for index, item in enumerate(agility_plan.objectives)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.leads is not None and len(agility_plan.leads) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="LEAD",
            )
            for index, item in enumerate(agility_plan.leads)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.sponsors is not None and len(agility_plan.sponsors) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="SPONSOR",
            )
            for index, item in enumerate(agility_plan.sponsors)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.coreteams is not None and len(agility_plan.coreteams) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="CORETEAM",
            )
            for index, item in enumerate(agility_plan.coreteams)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.coaches is not None and len(agility_plan.coaches) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="COACH",
            )
            for index, item in enumerate(agility_plan.coaches)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.users is not None and len(agility_plan.users) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="USER",
            )
            for index, item in enumerate(agility_plan.users)
        ]
        db.add_all(add_relation_items)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if agility_plan.roles is not None and len(agility_plan.roles) > 0:
        add_relation_items = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=agility_plan_id,
                related_id=item,
                relation_type="ROLE",
            )
            for index, item in enumerate(agility_plan.roles)
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
