from sqlalchemy import Column, Integer, String, ForeignKey
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
    job_ids = Column(ARRAY(Integer), default=[])
    role_ids = Column(ARRAY(Integer), default=[])
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

    @property
    def ordered_jobs(self):
        job_map = {job.id: job for job in self.jobs}
        ordered_jobs = [job_map[job_id] for job_id in self.job_ids]
        return ordered_jobs

    @property
    def ordered_roles(self):
        role_map = {role.id: role for role in self.roles}
        ordered_roles = [role_map[role_id] for role_id in self.role_ids]
        return ordered_roles
