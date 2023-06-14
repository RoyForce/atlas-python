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
                related_id=item.id,
                relation_type="ACTION",
            )
            for index, item in enumerate(agility_plan.actions)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    relation_count = db.query(models.AgilityPlanRelation).count() + 1
    if (
        agility_plan.objectives is not None
        and len(agility_plan.objectives) > 0
    ):
        db_agility_plan_relation_item = [
            models.AgilityPlanRelation(
                id=relation_count + index,
                agility_plan_id=db_agility_plan.id,
                related_id=items.id,
                relation_type="OBJECTIVE",
            )
            for index, items in enumerate(agility_plan.objectives)
        ]
        db.add_all(db_agility_plan_relation_item)
        db.commit()

    db.refresh(db_agility_plan)
    return db_agility_plan


def get_agility_plan_by_id(db: Session, agility_plan_id: int):
    agility_plan = (
        db.query(models.AgilityPlan)
        .filter(models.AgilityPlan.id == agility_plan_id)
        .one()
    )

    return agility_plan


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
