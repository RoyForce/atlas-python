from sqlalchemy import Column, Integer, String

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship


class Role(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    # jobs = relationship(
    #     "Job", secondary="job_role_mappings", back_populates="roles"
    # )
    # playbooks = relationship(
    #     "Playbook", secondary="playbook_role_mappings", back_populates="roles"
    # )
