from ctypes import Union
from pydantic import BaseModel, Field
import typing as t
from typing import List, Any, Dict, AnyStr
from enum import Enum


class TablesEnum(str, Enum):
    JOB_ROLE_MATRIX = "JOB_ROLE_MATRIX"
    SCREEN_JOB_MATRIX = "SCREEN_JOB_MATRIX"


class TableConfigBase(BaseModel):
    user_id: int = None
    table: TablesEnum = None
    config: Any = None


class TableConfigOut(TableConfigBase):
    pass


class TableConfigCreate(TableConfigBase):
    class Config:
        orm_mode = True


class TableConfigEdit(TableConfigBase):
    class Config:
        orm_mode = True


class TableConfig(TableConfigBase):
    id: int

    class Config:
        orm_mode = True
