from typing import List
from sqlalchemy import Column, Integer, String
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class UseCase(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "use_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    table_config = Column(String)
    job_ids = Column(ARRAY(Integer))
    role_ids = Column(ARRAY(Integer))
    jobs = relationship(
        "Job",
        primaryjoin="Job.id == any_(foreign(UseCase.job_ids))",
        uselist=True,
    )
    roles = relationship(
        "Role",
        primaryjoin="Role.id == any_(foreign(UseCase.role_ids))",
        uselist=True,
    )
