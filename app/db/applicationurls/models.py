from sqlalchemy import Column, Integer, String

from app.db.session import Base


class ApplicationUrl(Base):
    __tablename__ = "application_urls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
