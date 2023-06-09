from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship


class Action(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    action_type = Column(String, nullable=False)
