from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class Portfolio(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    team_id = Column(Integer)
    is_active = Column(Integer)
    description = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)
    source_update_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False)
