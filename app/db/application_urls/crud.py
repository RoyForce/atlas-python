from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas


def get_application_url(db: Session, application_url_id: int):
    application_url = (
        db.query(models.ApplicationUrl)
        .filter(models.ApplicationUrl.id == application_url_id)
        .first()
    )
    if not application_url:
        raise HTTPException(
            status_code=404, detail="Application URL not found"
        )
    return application_url


def get_application_urls(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.ApplicationUrlOut]:
    return db.query(models.ApplicationUrl).offset(skip).limit(limit).all()


def create_application_url(
    db: Session, application_url: schemas.ApplicationUrlCreate
):
    db_application_url = models.ApplicationUrl(
        name=application_url.name,
        url=application_url.url,
    )
    db.add(db_application_url)
    db.commit()
    db.refresh(db_application_url)
    return db_application_url


def delete_application_url(db: Session, application_url_id: int):
    application_url = get_application_url(db, application_url_id)
    if not application_url:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Application URL not found"
        )
    db.delete(application_url)
    db.commit()
    return application_url


def edit_application_url(
    db: Session,
    application_url_id: int,
    application_url: schemas.ApplicationUrlEdit,
) -> schemas.ApplicationUrl:
    db_application_url = get_application_url(db, application_url_id)
    if not db_application_url:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Application URL not found"
        )
    update_data = application_url.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_application_url, key, value)

    db.add(db_application_url)
    db.commit()
    db.refresh(db_application_url)
    return db_application_url
