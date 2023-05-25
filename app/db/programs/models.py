from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin, ExternalSource
from sqlalchemy.orm import relationship


class Program(Base, CoreBase, TrackTimeMixin, ExternalSource):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=True)
    teams = relationship(
        "Team",
        primaryjoin="Program.id == Team.program_id",
        uselist=True,
    )
