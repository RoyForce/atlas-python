from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin, ExternalSource
from sqlalchemy.orm import relationship


class Sprint(Base, CoreBase, TrackTimeMixin, ExternalSource):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    short_name = Column(String, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    release_id = Column(Integer, ForeignKey("releases.id"), nullable=True)
    begin_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    actual_end_date = Column(DateTime, nullable=True)
