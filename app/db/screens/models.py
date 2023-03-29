from typing import List
from sqlalchemy import Column, Integer, String
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class Screen(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    screen_url = Column(String, nullable=True)
    job_ids = Column(ARRAY(Integer), default=[])
    jobs = relationship(
        "Job",
        primaryjoin="Job.id == any_(foreign(Screen.job_ids))",
        uselist=True,
    )
