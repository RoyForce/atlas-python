from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from fastapi.encoders import jsonable_encoder


def get_table_config(db: Session, table_config_id: int):
    table_config = (
        db.query(models.TableConfig)
        .filter(models.TableConfig.id == table_config_id)
        .first()
    )
    if not table_config:
        raise HTTPException(status_code=404, detail="Table config not found")
    return table_config


def get_table_configs(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.TableConfigOut]:
    return db.query(models.TableConfig).offset(skip).limit(limit).all()


def create_table_config(db: Session, table_config: schemas.TableConfigCreate):
    db_table_config = models.TableConfig(
        user_id=table_config.user_id,
        table=table_config.table,
        config=jsonable_encoder(table_config.config),
    )

    db.add(db_table_config)
    db.commit()
    db.refresh(db_table_config)
    return db_table_config


def delete_table_config(db: Session, table_config_id: int):
    table_config = get_table_config(db, table_config_id)
    if not table_config:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="TableConfig not found"
        )
    db.delete(table_config)
    db.commit()
    return table_config


def edit_table_config(
    db: Session, table_config_id: int, table_config: schemas.TableConfigEdit
) -> schemas.TableConfig:
    db_table_config = get_table_config(db, table_config_id)
    if not db_table_config:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Table config not found"
        )
    update_data = table_config.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "config":
            value = jsonable_encoder(value)
        setattr(db_table_config, key, value)

    db.add(db_table_config)
    db.commit()
    db.refresh(db_table_config)
    return db_table_config
