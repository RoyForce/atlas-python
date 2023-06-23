from typing import List
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Numeric,
)
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class Measurement(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Numeric)
    objective_id = Column(ForeignKey("objectives.id"))
