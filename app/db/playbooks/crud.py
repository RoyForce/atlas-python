from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from fastapi.encoders import jsonable_encoder
from . import models, schemas


def get_playbook(db: Session, playbook_id: int):
    playbook = (
        db.query(models.Playbook)
        .filter(models.Playbook.id == playbook_id)
        .first()
    )
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    return playbook


def get_playbooks(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.PlaybookOut]:
    return db.query(models.Playbook).offset(skip).limit(limit).all()


def create_playbook(db: Session, playbook: schemas.PlaybookCreate):

    # playbook_data = jsonable_encoder(playbook)
    # db_playbook = models.Playbook(**playbook_data)

    db_playbook = models.Playbook(
        name=playbook.name,
        description=playbook.description,
        page_content=playbook.page_content,
    )

    db.add(db_playbook)
    db.commit()

    if playbook.role_ids is not None and len(playbook.role_ids) > 0:
        db_playbook_roles = [
            models.PlaybookRole(playbook_id=db_playbook.id, role_id=role_id)
            for role_id in playbook.role_ids
        ]
        db.add_all(db_playbook_roles)
        db.commit()

    db.refresh(db_playbook)
    return db_playbook


def delete_playbook(db: Session, playbook_id: int):
    playbook = get_playbook(db, playbook_id)
    if not playbook:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Playbook not found"
        )
    db.delete(playbook)
    db.commit()
    return playbook


def edit_playbook(
    db: Session, playbook_id: int, playbook: schemas.PlaybookEdit
) -> schemas.Playbook:
    db_playbook = get_playbook(db, playbook_id)
    if not db_playbook:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Playbook not found"
        )
    update_data = playbook.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "role_ids":
            delete_playbook_role(db, db_playbook.id)
            db_playbook_roles = [
                models.PlaybookRole(
                    playbook_id=db_playbook.id, role_id=role_id
                )
                for role_id in value
            ]
            db.add_all(db_playbook_roles)
            db.commit()
        else:
            setattr(db_playbook, key, value)

    db.add(db_playbook)
    db.commit()

    db.refresh(db_playbook)
    return db_playbook


def delete_playbook_role(db: Session, playbook_id: int):
    playbook_roles = get_playbook_roles(db, playbook_id)
    if playbook_roles:
        for value in playbook_roles:
            db.delete(value)
    db.commit()
    return playbook_roles


def get_playbook_roles(db: Session, playbook_id: int):
    playbook_roles = (
        db.query(models.PlaybookRole)
        .filter(models.PlaybookRole.playbook_id == playbook_id)
        .all()
    )
    if playbook_roles:
        return playbook_roles
