from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin, ExternalSource


class CostCenter(Base, CoreBase, TrackTimeMixin, ExternalSource):
    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hr_rate = Column(Integer)
    description = Column(String, nullable=True)
