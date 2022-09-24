from ctypes import Union
from email.mime import application
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase

from app import db
from typing import List


class JobRole(Base):
    __tablename__ = "job_role_mappings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column("job_id", ForeignKey("jobs.id"), primary_key=True)
    role_id = Column("role_id", ForeignKey("roles.id"), primary_key=True)


class Job(Base, CoreBase):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    application_url_id = Column(
        Integer, ForeignKey("application_urls.id"), nullable=True
    )
    steps = Column(JSONB, nullable=True)
    is_locked = Column(Boolean)
    roles = relationship(
        "Role", secondary="job_role_mappings", back_populates="jobs"
    )
    application_url = relationship("ApplicationUrl", backref="jobs")

    @property
    def role_ids(self) -> List[int]:
        return [role.id for role in self.roles]
