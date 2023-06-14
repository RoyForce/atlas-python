from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON


class Assessment(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    dimensions = relationship(
        "Dimension",
        primaryjoin="Assessment.id == Dimension.assessment_id",
        uselist=True,
    )
