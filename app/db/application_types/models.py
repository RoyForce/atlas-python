from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class ApplicationType(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "application_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    created_by_user = relationship(
        "User",
        primaryjoin="ApplicationType.created_by == User.id",
        uselist=False,
    )
    updated_by_user = relationship(
        "User",
        primaryjoin="ApplicationType.updated_by == User.id",
        uselist=False,
    )
