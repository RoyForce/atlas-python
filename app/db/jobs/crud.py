from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
import typing as t
from . import models, schemas
from app.db.users.crud import get_user
from app.core import security
from app.db.use_cases.models import UseCase
from sqlalchemy.orm.attributes import flag_modified


def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


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


def format_job_steps(job):
    update_data = job.dict(exclude_unset=True)
    if "steps" in update_data:
        if update_data["steps"] is None:
            update_data["steps"] = {}
        steps = {k.decode(): v for k, v in update_data["steps"].items()}
        setattr(job, "steps", steps)
    return job


def delete_job_mapping(db: Session, job_id: int):
    # delete job mapping in use case
    affected_use_cases = (
        db.query(UseCase).filter(UseCase.job_ids.any(job_id)).all()
    )
    for use_case in affected_use_cases:
        use_case.job_ids.remove(job_id)
        flag_modified(use_case, "job_ids")
        db.merge(use_case)
        db.flush()
        db.commit()
