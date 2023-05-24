from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship


class Role(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)
    source_update_at = Column(DateTime, nullable=True)
    created_by = Column(Boolean, nullable=True)
    updated_by = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, default=False)

    jobs = relationship(
        "Job",
        primaryjoin="Role.id == any_(foreign(Job.role_ids))",
    )
    playbooks = relationship(
        "Playbook",
        primaryjoin="Role.id == any_(foreign(Playbook.role_ids))",
    )
    use_cases = relationship(
        "UseCase",
        primaryjoin="Role.id == any_(foreign(UseCase.role_ids))",
    )

    @property
    def job_ids(self):
        return [job.id for job in self.jobs]

    @property
    def playbook_ids(self):
        return [playbook.id for playbook in self.playbooks]

    @property
    def use_case_ids(self):
        return [use_case.id for use_case in self.use_cases]

    @job_ids.setter
    def job_ids(self, job_ids):
        pass

    @playbook_ids.setter
    def playbook_ids(self, playbook_ids):
        pass

    @use_case_ids.setter
    def use_case_ids(self, use_case_ids):
        pass
