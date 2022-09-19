from ctypes import Union
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

from app import db


class JobRole(Base):
    __tablename__ = "job_role_mappings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column("job_id", ForeignKey("jobs.id"), primary_key=True)
    role_id = Column("role_id", ForeignKey("roles.id"), primary_key=True)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    application_url_id = Column(Integer, nullable=False)
    # steps = Column(JSONB)
    is_locked = Column(Boolean)
    roles = relationship(
        "Role", secondary="job_role_mappings", back_populates="jobs"
    )
