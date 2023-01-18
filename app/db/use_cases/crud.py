from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from . import models, schemas


def get_use_case(db: Session, use_case_id: int):
    return (
        db.query(models.UseCase)
        .filter(models.UseCase.id == use_case_id)
        .first()
    )


def create_use_case(db: Session, use_case: schemas.UseCaseCreate):
    db_use_case = models.UseCase(
        name=use_case.name,
        description=use_case.description,
        table_config=use_case.table_config,
    )

    db.add(db_use_case)
    db.commit()

    if (
        use_case.role_ids is not None
        and len(use_case.role_ids) > 0
        and use_case.job_ids is not None
        and len(use_case.job_ids) > 0
    ):
        for role_id in use_case.role_ids:
            db_use_case_roles = [
                models.UseCaseMapping(
                    use_case_id=db_use_case.id, role_id=role_id, job_id=job_id
                )
                for job_id in use_case.job_ids
            ]
            db.add_all(db_use_case_roles)
            db.commit()

    db.refresh(db_use_case)
    return db_use_case


def edit_use_case(
    db: Session, use_case_id: int, use_case: schemas.UseCaseEdit
) -> schemas.UseCase:
    db_use_case = get_use_case(db, use_case_id)
    if not db_use_case:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="UseCase not found"
        )
    update_data = use_case.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "role_ids":
            if (
                use_case.role_ids is not None
                and len(use_case.role_ids) > 0
                and use_case.job_ids is not None
                and len(use_case.job_ids) > 0
            ):
                delete_use_case_role_job(db, db_use_case.id)
                for role_id in use_case.role_ids:
                    db_use_case_roles = [
                        models.UseCaseMapping(
                            use_case_id=db_use_case.id,
                            role_id=role_id,
                            job_id=job_id,
                        )
                        for job_id in use_case.job_ids
                    ]
                    db.add_all(db_use_case_roles)
                    db.commit()
        else:
            if key != "job_ids":
                setattr(db_use_case, key, value)

    db.add(db_use_case)
    db.commit()

    db.refresh(db_use_case)
    return db_use_case


def delete_use_case_role_job(db: Session, use_case_id: int):
    use_case_roles = get_use_case_roles_jobs(db, use_case_id)
    if use_case_roles:
        for value in use_case_roles:
            db.delete(value)
    db.commit()
    return use_case_roles


def get_use_case_roles_jobs(db: Session, use_case_id: int):
    use_case_roles = (
        db.query(models.UseCaseMapping)
        .filter(models.UseCaseMapping.use_case_id == use_case_id)
        .all()
    )
    if use_case_roles:
        return use_case_roles


def get_use_case_mappings(db: Session, type: str, id: int):
    if type == "job":
        data = (
            db.query(models.UseCaseMapping)
            .filter(models.UseCaseMapping.job_id == id)
            .all()
        )
        return data if data else False

    elif type == "roles":
        data = (
            db.query(models.UseCaseMapping)
            .filter(models.UseCaseMapping.role_id == id)
            .all()
        )
        return data if data else False
