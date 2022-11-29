from ctypes import Union
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase
from typing import List
from app import db


class UseCaseMapping(Base):
    __tablename__ = "use_cases_mappings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    use_case_id = Column(
        "use_case_id", ForeignKey("use_cases.id"), primary_key=True
    )
    job_id = Column("job_id", ForeignKey("jobs.id"), primary_key=True)
    role_id = Column("role_id", ForeignKey("roles.id"), primary_key=True)


class UseCase(Base, CoreBase):
    __tablename__ = "use_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    table_config = Column(String)
    roles = relationship(
        "Role", secondary="use_cases_mappings", back_populates="use_cases"
    )
    jobs = relationship(
        "Job", secondary="use_cases_mappings", back_populates="use_cases"
    )

    @property
    def role_ids(self) -> List[int]:
        return [role.id for role in self.roles]

    @property
    def job_ids(self) -> List[int]:
        return [job.id for job in self.jobs]

    @property
    def use_case_mapping(self) -> List[UseCaseMapping]:
        return UseCaseMapping.query.filter_by(use_case_id=self.id).all()
