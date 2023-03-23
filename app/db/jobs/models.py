from email.policy import default
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin

from typing import List


class JobRole(Base):
    __tablename__ = "job_role_mappings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column("job_id", ForeignKey("jobs.id"), primary_key=True)
    role_id = Column("role_id", ForeignKey("roles.id"), primary_key=True)


class Job(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    application_url_id = Column(
        Integer, ForeignKey("application_urls.id"), nullable=True
    )
    steps = Column(JSONB, nullable=True, default={})
    is_locked = Column(Boolean, default=False)
    roles = relationship(
        "Role", secondary="job_role_mappings", back_populates="jobs"
    )
    application_url = relationship(
        "ApplicationUrl", lazy="subquery", backref="jobs"
    )
    is_template = Column(Boolean, default=False)

    @property
    def role_ids(self) -> List[int]:
        return [role.id for role in self.roles]
