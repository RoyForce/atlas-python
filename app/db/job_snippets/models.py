from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class JobSnippet(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "job_snippets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    steps = Column(JSON, nullable=True, default={})
