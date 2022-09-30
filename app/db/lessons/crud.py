from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas


def get_lesson(db: Session, lesson_id: int):
    lesson = (
        db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    )
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


def get_lessons(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.LessonOut]:
    return db.query(models.Lesson).offset(skip).limit(limit).all()


def create_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(
        name=lesson.name,
        description=lesson.description,
        duration=lesson.duration,
        page_content=lesson.page_content,
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def delete_lesson(db: Session, lesson_id: int):
    lesson = get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Lesson not found"
        )
    db.delete(lesson)
    db.commit()
    return lesson


def edit_lesson(
    db: Session, lesson_id: int, lesson: schemas.LessonEdit
) -> schemas.Lesson:
    db_lesson = get_lesson(db, lesson_id)
    if not db_lesson:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Lesson not found"
        )
    update_data = lesson.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_lesson, key, value)

    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson
