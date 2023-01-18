from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas


def get_playbook(db: Session, playbook_id: int):
    return (
        db.query(models.Playbook)
        .filter(models.Playbook.id == playbook_id)
        .first()
    )


def create_playbook(db: Session, playbook: schemas.PlaybookCreate):
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


def get_playbook_by_role(db: Session, role_id: int):
    playbook_roles = (
        db.query(models.PlaybookRole)
        .filter(models.PlaybookRole.role_id == role_id)
        .all()
    )
    if playbook_roles:
        return playbook_roles
