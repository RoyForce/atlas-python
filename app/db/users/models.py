from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class User(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(Integer)
    cost_center_id = Column(Integer)
    is_designer = Column(Boolean, default=False)
    source_id = Column(Integer, nullable=True)
    source_update_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    @property
    def name(self):
        return f"{self.first_name if self.first_name else ''} {self.last_name if self.last_name else ''}".strip()
