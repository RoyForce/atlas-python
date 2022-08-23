from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas


def get_role(db: Session, role_id: int):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def get_roles(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.RoleOut]:
    return db.query(models.Role).offset(skip).limit(limit).all()


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(
        name=role.name,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Role not found")
    db.delete(role)
    db.commit()
    return role


def edit_role(
    db: Session, role_id: int, role: schemas.RoleEdit
) -> schemas.Role:
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Role not found")
    update_data = role.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_role, key, value)

    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
