# from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import Session
from typing import List, Union
from fastapi import HTTPException


class CoreBase(object):
    def dict(self, exclude: Union[List[str], None] = []):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }


def get_lists(db: Session, model, query_params):
    query_params = dict(query_params)
    if all(key in query_params for key in ("_start", "_end")):
        skip = int(query_params["_start"])
        limit = int(query_params["_end"]) - skip
        return db.query(model).offset(skip).limit(limit).all()
    else:
        return db.query(model).all()


def get_item(db: Session, model, id: int):
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def create_item(db: Session, model, item: dict):
    db_item = model(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, model, id: int):
    item = get_item(db, model, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return item


def edit_item(db: Session, model, id: int, item: dict):
    db_item = get_item(db, model, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    return db_item
