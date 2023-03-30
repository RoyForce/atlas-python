from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class ApplicationUrl(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "application_urls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    url = Column(String)
    application_type_id = Column(
        Integer, ForeignKey("application_types.id"), nullable=True
    )
    application_type = relationship(
        "ApplicationType", lazy="subquery", backref="application_urls"
    )
