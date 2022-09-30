from sqlalchemy import Column, Integer, String

from app.db.session import Base
from app.db.core import CoreBase
from sqlalchemy.orm import relationship


class Lesson(Base, CoreBase):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    page_content = Column(String, nullable=True)
