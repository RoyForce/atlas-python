from typing import List
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
)
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from fastapi import HTTPException
from app.db.enums import MetricsType


class Objective(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "objectives"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)
    metrics_type = Column(String, nullable=False)
    start_value = Column(Numeric)
    target_value = Column(Numeric)
    agility_plan_id = Column(ForeignKey("agility_plans.id"))
    stwert = Column(ForeignKey("users.id"))
    results = relationship(
        "Result",
        primaryjoin="Objective.id == Result.objective_id",
        uselist=True,
    )

    @orm.validates("start_value", "target_value")
    def validate_values(self, key, value):
        if self.metrics_type == MetricsType.PERCENTAGE:
            if not 0 <= value <= 100:
                raise HTTPException(status_code=406, detail="Invalid Value")
            return value
        else:
            if not 0 <= value:
                raise HTTPException(status_code=406, detail="Invalid Value")
            return value
