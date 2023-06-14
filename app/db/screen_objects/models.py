from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON


class ScreenObject(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "screen_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    properties = Column(JSON, default={})
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
