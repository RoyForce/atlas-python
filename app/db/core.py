from datetime import datetime
from sqlalchemy import (
    Column,
    desc,
    TIMESTAMP,
    text,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import Session
from typing import List, Union
from fastapi import HTTPException
from sqlalchemy.inspection import inspect


from sqlalchemy.dialects.postgresql import JSON, JSONB


class TrackTimeMixin:
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
    )


class ExternalSource:
    source_id = Column(Integer, nullable=True)
    source_update_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False)


class CoreBase(object):
    def dict(self, exclude: Union[List[str], None] = []):
        json_object = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }
        for arg in json_object:
            if isinstance(json_object[arg], datetime):
                json_object[arg] = json_object[arg].isoformat()
        return json_object


def get_lists(db: Session, model, query_params):
    query_params = dict(query_params)
    sort = query_params["_sort"] if "_sort" in query_params else "updated_at"
    order = query_params["_order"] if "_order" in query_params else "desc"

    query = db.query(model)
    attr = getattr(model, sort, None)

    if attr:
        if type(attr.property).__name__ == "RelationshipProperty":
            """If sort is a relationship"""
            foreign_modal = attr.property.mapper.class_
            foreign_attr = getattr(foreign_modal, "name", None)
            if foreign_attr:
                order_by = (
                    desc(foreign_attr) if order == "desc" else foreign_attr
                )
                query = query.join(attr).order_by(order_by)
        else:
            """If sort is an attribute"""
            order_by = desc(attr) if order == "desc" else attr
            query = query.order_by(order_by)
    else:
        if "." in sort:
            """If sort is a relationship with a dot notation"""
            sort = sort.split(".")
            relations = inspect(model).relationships.items()
            attr = None
            foreign_modal = None
            for relation in relations:
                if relation[0] == sort[0]:
                    attr = getattr(model, relation[1].key)
                    foreign_modal = attr.mapper.class_
                    break

            if attr and foreign_modal:
                foreign_attr = getattr(foreign_modal, sort[1], None)
                if foreign_attr:
                    order_by = (
                        desc(foreign_attr) if order == "desc" else foreign_attr
                    )
                    query = query.join(attr).order_by(order_by)

    return query.all()

    # if all(key in query_params for key in ("_start", "_end")):
    #     skip = int(query_params["_start"])
    #     limit = int(query_params["_end"]) - skip
    #     return query.offset(skip).limit(limit).all()
    # else:
    #     return query.all()


def get_item(db: Session, model, id: int):
    item = db.query(model).filter(model.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def sanitize_json_values(model, item: dict):
    for column in model.__table__.columns:
        if (
            isinstance(column.type, JSON) or isinstance(column.type, JSONB)
        ) and column.name in item.dict():
            if isinstance(item.dict()[column.name], dict):
                setattr(
                    item,
                    column.name,
                    {
                        k.decode(): v
                        for k, v in item.dict()[column.name].items()
                    },
                )
    return item


def create_item(db: Session, model, item: dict):
    item = sanitize_json_values(model, item)
    db_item = model(**item.dict(exclude_unset=True))
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

    item = sanitize_json_values(model, item)
    update_data = item.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    return db_item
