from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas


def get_applicationurl(db: Session, applicationurl_id: int):
    applicationurl = db.query(models.ApplicationUrl).filter(models.ApplicationUrl.id == applicationurl_id).first()
    if not applicationurl:
        raise HTTPException(status_code=404, detail="Application URL not found")
    return applicationurl


def get_applicationurls(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.ApplicationUrlOut]:
    return db.query(models.ApplicationUrl).offset(skip).limit(limit).all()


def create_applicationurl(db: Session, applicationurl: schemas.ApplicationUrlCreate):
    db_applicationurl = models.ApplicationUrl(
        name=applicationurl.name,
        url=applicationurl.url,
    )
    db.add(db_applicationurl)
    db.commit()
    db.refresh(db_applicationurl)
    return db_applicationurl


def delete_applicationurl(db: Session, applicationurl_id: int):
    applicationurl = get_applicationurl(db, applicationurl_id)
    if not applicationurl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Application URL not found")
    db.delete(applicationurl)
    db.commit()
    return applicationurl


def edit_applicationurl(
    db: Session, applicationurl_id: int, applicationurl: schemas.ApplicationUrlEdit
) -> schemas.ApplicationUrl:
    db_applicationurl = get_applicationurl(db, applicationurl_id)
    if not db_applicationurl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Application URL not found")
    update_data = applicationurl.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_applicationurl, key, value)

    db.add(db_applicationurl)
    db.commit()
    db.refresh(db_applicationurl)
    return db_applicationurl
