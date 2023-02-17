from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from app.db.session import Base
from app.db.core import CoreBase
from sqlalchemy.orm import relationship
from app.db.core import CoreBase, TrackTimeMixin


class CourseItems(Base):
    __tablename__ = "course_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column("course_id", ForeignKey("courses.id"), primary_key=True)
    item_title = Column("item_title", String, nullable=True)
    item_type = Column("item_type", String, nullable=True)
    item_id = Column("item_id", Integer, nullable=True)
    item_order = Column("item_order", Integer, nullable=True)
    courses = relationship("Course", back_populates="items")


class Course(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    enroll_required = Column(Boolean, default=False)
    passing_percentage = Column(Integer, nullable=True)
    items = relationship("CourseItems", back_populates="courses")
