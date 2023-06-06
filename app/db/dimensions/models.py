from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from fastapi import HTTPException


class Dimension(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "dimensions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    assessment_id = Column(
        Integer, ForeignKey("assessments.id"), nullable=True
    )
    ideal_value = Column(
        Integer, CheckConstraint("ideal_value >= -5 AND ideal_value <= 5")
    )
    baseline_value = Column(
        Integer,
        CheckConstraint("baseline_value >= -5 AND baseline_value <= 5"),
    )
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    questions = relationship(
        "Question",
        primaryjoin="Dimension.id == Question.dimension_id",
        uselist=True,
    )

    @orm.validates("baseline_value", "ideal_value")
    def validate_values(self, key, value):
        if not -5 <= value <= 5:
            raise HTTPException(status_code=406, detail="Invalid Value")
        return value
