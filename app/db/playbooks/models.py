from ctypes import Union
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

from app import db


class PlaybookRole(Base):
    __tablename__ = "playbook_role_mappings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    playbook_id = Column(
        "playbook_id", ForeignKey("playbooks.id"), primary_key=True
    )
    role_id = Column("role_id", ForeignKey("roles.id"), primary_key=True)


class Playbook(Base):
    __tablename__ = "playbooks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    page_content = Column(String)
    roles = relationship(
        "Role", secondary="playbook_role_mappings", back_populates="playbooks"
    )
