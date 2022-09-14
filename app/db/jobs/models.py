from ctypes import Union
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    application_url_id = Column(Integer, nullable=False)
    # steps = Column(JSONB)
    is_locked = Column(Boolean)
