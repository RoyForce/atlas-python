from email.policy import default
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.dialects.postgresql import ARRAY


class Job(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    steps = Column(JSON, nullable=True, default={})
    is_locked = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)

    application_url_id = Column(
        Integer, ForeignKey("application_urls.id"), nullable=True
    )
    application_url = relationship(
        "ApplicationUrl", lazy="subquery", backref="jobs"
    )
    application_type_id = Column(
        Integer, ForeignKey("application_types.id"), nullable=True
    )
    application_type = relationship(
        "ApplicationType", lazy="subquery", backref="jobs"
    )
    role_ids = Column(ARRAY(Integer), default=[])
    roles = relationship(
        "Role",
        primaryjoin="Role.id == any_(foreign(Job.role_ids))",
        uselist=True,
    )
    screens = relationship(
        "Screen",
        primaryjoin="Job.id == any_(foreign(Screen.job_ids))",
    )

    @property
    def screen_ids(self):
        return [screen.id for screen in self.screens]

    @screen_ids.setter
    def screen_ids(self, screen_ids):
        pass
