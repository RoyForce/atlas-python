from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class TableConfig(Base):
    __tablename__ = "user_table_views"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    table = Column(String, nullable=False)
    config = Column(JSONB, nullable=True)
