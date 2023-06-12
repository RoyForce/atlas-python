from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin, ExternalSource
from sqlalchemy.orm import relationship


class Portfolio(Base, CoreBase, TrackTimeMixin, ExternalSource):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    is_active = Column(Integer)
    description = Column(String, nullable=True)
    programs = relationship(
        "Program",
        primaryjoin="Portfolio.id == Program.portfolio_id",
        uselist=True,
    )
    created_by_user = relationship(
        "User",
        primaryjoin="Portfolio.created_by == User.id",
        uselist=False,
    )
    updated_by_user = relationship(
        "User",
        primaryjoin="Portfolio.updated_by == User.id",
        uselist=False,
    )
