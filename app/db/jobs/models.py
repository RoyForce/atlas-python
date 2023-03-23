from email.policy import default
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.dialects.postgresql import ARRAY

from typing import List


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
    role_ids = Column(ARRAY(Integer))
    roles = relationship(
        "Role",
        primaryjoin="Role.id == any_(foreign(Job.role_ids))",
        uselist=True,
    )
    application_url = relationship(
        "ApplicationUrl", lazy="subquery", backref="jobs"
    )
    is_template = Column(Boolean, default=False)
