from sqlalchemy import Column, Integer, String

from app.db.session import Base
from app.db.core import CoreBase


class ApplicationUrl(Base, CoreBase):
    __tablename__ = "application_urls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    url = Column(String)
