from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from app.db.jobs.crud import get_job_roles
from app.db.use_cases.crud import get_use_case_mappings
from app.db.playbooks.crud import get_playbook_by_role
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
    delete_role_mapping(db, role_id)
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


def delete_role_mapping(db: Session, role_id: int):
    type = "roles"
    job_roles = get_job_roles(db, type, role_id)
    if job_roles:
        for value in job_roles:
            db.delete(value)
            db.commit()
    use_case_resp = get_use_case_mappings(db, type, role_id)
    if use_case_resp:
        for value in use_case_resp:
            db.delete(value)
            db.commit()
    playbook_resp = get_playbook_by_role(db, role_id)
    if playbook_resp:
        for value in playbook_resp:
            db.delete(value)
            db.commit()
    return True
