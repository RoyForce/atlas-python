from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship


class Lesson(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    page_content = Column(String, nullable=True)
    is_template = Column(Boolean, default=False)
    created_by_user = relationship(
        "User",
        primaryjoin="Lesson.created_by == User.id",
        uselist=False,
    )
    updated_by_user = relationship(
        "User",
        primaryjoin="Lesson.updated_by == User.id",
        uselist=False,
    )
