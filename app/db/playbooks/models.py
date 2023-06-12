from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class Playbook(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "playbooks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    page_content = Column(String)
    role_ids = Column(ARRAY(Integer), default=[])
    roles = relationship(
        "Role",
        primaryjoin="Role.id == any_(foreign(Playbook.role_ids))",
        uselist=True,
    )
    created_by_user = relationship(
        "User",
        primaryjoin="Playbook.created_by == User.id",
        uselist=False,
    )
    updated_by_user = relationship(
        "User",
        primaryjoin="Playbook.updated_by == User.id",
        uselist=False,
    )
