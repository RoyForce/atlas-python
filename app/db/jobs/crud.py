from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
import typing as t
from fastapi.encoders import jsonable_encoder
from . import models, schemas
from app.db.users.crud import get_user
from app.core import security


def get_job(db: Session, job_id: int):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job


def get_jobs(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.JobOut]:
    return db.query(models.Job).offset(skip).limit(limit).all()


def create_job(db: Session, job: schemas.JobCreate):

    # job_data = jsonable_encoder(job)
    # db_job = models.Job(**job_data)

    db_job = models.Job(
        name=job.name,
        description=job.description,
        application_url_id=job.application_url_id,
        is_template=job.is_template,
    )

    db.add(db_job)
    db.commit()

    if job.role_ids is not None and len(job.role_ids) > 0:
        db_job_roles = [
            models.JobRole(job_id=db_job.id, role_id=role_id)
            for role_id in job.role_ids
        ]
        db.add_all(db_job_roles)
        db.commit()

    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(job)
    db.commit()
    return job


def edit_job(db: Session, job_id: int, job: schemas.JobEdit) -> schemas.Job:
    db_job = get_job(db, job_id)
    if not db_job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    update_data = job.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "role_ids":
            delete_job_role(db, db_job.id)
            db_job_roles = [
                models.JobRole(job_id=db_job.id, role_id=role_id)
                for role_id in value
            ]
            db.add_all(db_job_roles)
            db.commit()
        else:
            setattr(db_job, key, value)

    db.add(db_job)
    db.commit()

    db.refresh(db_job)
    return db_job


def validate_extension_token(request: Request):
    if f"Bearer {security.EXTENSION_TOKEN}" != request.headers.get(
        "Authorization"
    ):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Invalid extension token."
        )


def validate_user_and_job(db: Session, job_id, user_id, mode):

    user = get_user(db, user_id)
    if mode == schemas.ExtensionMode.DESIGNER and not user.is_designer:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="User has no designer access."
        )

    job = get_job(db, job_id)
    if job.is_locked:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Job is locked by another user."
        )

    return job


def delete_job_role(db: Session, job_id: int):
    job_roles = get_job_roles(db, job_id)
    if job_roles:
        for value in job_roles:
            db.delete(value)
    db.commit()
    return job_roles


def get_job_roles(db: Session, job_id: int):
    job_roles = (
        db.query(models.JobRole).filter(models.JobRole.job_id == job_id).all()
    )
    if job_roles:
        return job_roles
