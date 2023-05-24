from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class Team(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    program_id = Column(Integer)
    type = Column(Integer)
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    sprint_prefix = Column(String, nullable=True)
    short_name = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)
    source_update_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, default=False)
    user_ids = Column(ARRAY(Integer), default=[])
