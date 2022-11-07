from sqlalchemy import Column, Integer, String

from app.db.session import Base
from app.db.core import CoreBase
from sqlalchemy.orm import relationship


class Role(Base, CoreBase):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    jobs = relationship(
        "Job", secondary="job_role_mappings", back_populates="roles"
    )
    playbooks = relationship(
        "Playbook", secondary="playbook_role_mappings", back_populates="roles"
    )
    use_cases = relationship(
        "UseCase", secondary="use_cases_mappings", back_populates="roles"
    )
