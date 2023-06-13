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
        actions=agility_plan.actions,
        objectives=agility_plan.objectives,
        users=agility_plan.users,
        roles=agility_plan.roles,
        leads=agility_plan.leads,
        sponsors=agility_plan.sponsors,
        coreteams=agility_plan.coreteams,
        coaches=agility_plan.coaches,
        organizations=agility_plan.organizations,
        created_by=agility_plan.created_by,
    )
    db.add(db_agility_plan)
    db.commit()

    if agility_plan.actions is not None and len(agility_plan.actions) > 0:
        db_agility_plan_action_item = [
            models.Action(
                item_id=items.item_id,
                item_title=items.item_title,
                item_type=items.item_action_type,
                item_order=items.item_order,
            )
            for items in agility_plan.actions
        ]
        db.add_all(db_agility_plan_action_item)
        db.commit()

    if agility_plan.objectives is not None and len(agility_plan.objectives) > 0:
        db_agility_plan_objective_item = [
            models.Objective(
                item_id=items.item_id,
                item_title=items.item_title,
                item_type=items.item_metrics_type,
                item_start_value=items.item_start_value,
                item_target_value=items.item_target_value,
                item_order=items.item_order,
            )
            for items in agility_plan.objectives
        ]
        db.add_all(db_agility_plan_objective_item)
        db.commit()

    db.refresh(db_agility_plan)
    return db_agility_plan


def edit_course(
    db: Session, course_id: int, course: schemas.AgilityPlanEdit
) -> schemas.Course:
    course_item = get_course_item(db, course_id)
    db_course = (
        db.query(models.Course).filter(models.Course.id == course_id).first()
    )
    if not db_course:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    update_data = course.dict(exclude_unset=True)

    items_to_delete = [
        db_item.id
        for db_item in db_course.items
        if db_item.id not in [item.id for item in course.items]
    ]
    delete_extra_course_items(db, items_to_delete)

    for key, value in update_data.items():
        if key == "items":
            for item in value:
                if "id" in item:
                    course_item = (
                        db.query(models.CourseItems)
                        .filter(models.CourseItems.id == item["id"])
                        .first()
                    )
                    if course_item:
                        setattr(course_item, "item_order", item["item_order"])
                else:
                    item_id = 0
                    if item["item_type"] == "LESSON":
                        resp = get_lesson_by_name_create_if_none(
                            db, item["item_title"]
                        )
                        item_id = resp.id
                    db_course_items = models.CourseItems(
                        course_id=db_course.id,
                        item_type=item["item_type"],
                        item_title=item["item_title"],
                        item_id=item_id,
                        item_order=item["item_order"],
                    )
                    db.add(db_course_items)
                    db.commit()

        else:
            setattr(db_course, key, value)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_related_item(db: Session, agility_plan_id: int, type: str):
    response: Any = None
    if type == "ACTION":
        response = (
            db.query(models.Action)
            .filter(models.Action.course_id == agility_plan_id)
            .all()
        )
    course = (
        db.query(models.CourseItems)
        .filter(models.CourseItems.course_id == agility_plan_id)
        .all()
    )
    if course:
        return course


def get_course_item_by_id(db: Session, id: int):
    course = db.query(models.CourseItems).get(id)
    if course:
        return course


def delete_extra_course_items(db: Session, item_to_delete: any):
    course_item = (
        db.query(models.CourseItems)
        .filter(models.CourseItems.id.in_(item_to_delete))
        .all()
    )
    # db.delete(course)
    for item_row in course_item:
        db.delete(item_row)
        if item_row.item_type == "LESSON":
            delete_item(db, Lesson, item_row.item_id)
    db.commit()
    return True


def get_lesson_by_name_create_if_none(db: Session, name: str):
    lesson = db.query(Lesson).filter(Lesson.name == name).first()
    if not lesson:
        db_lesson = Lesson(name=name, is_template=False)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson
    return lesson
