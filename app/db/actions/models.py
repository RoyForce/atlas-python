from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    action_type = Column(String, nullable=False)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_active = Column(Boolean)
    action_type = Column(String)
    playbook_id = Column(Integer)
