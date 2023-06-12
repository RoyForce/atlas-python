from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin, ExternalSource
from sqlalchemy.orm import relationship
from app.db.users.models import User


class Team(Base, CoreBase, TrackTimeMixin, ExternalSource):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    type = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_kanban_team = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    sprint_prefix = Column(String, nullable=True)
    short_name = Column(String, nullable=True)
    user_ids = Column(ARRAY(Integer), default=[])
    users = relationship(
        "User",
        primaryjoin="User.id == any_(foreign(Team.user_ids))",
        uselist=True,
        lazy="noload",
    )
