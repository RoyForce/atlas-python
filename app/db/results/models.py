from typing import List
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
)
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy import orm
from sqlalchemy.orm import relationship


class Result(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(Integer, ForeignKey("objectives.id"), nullable=True)
    value = Column(Numeric)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
