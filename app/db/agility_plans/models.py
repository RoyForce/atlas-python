from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class AgilityPlan(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "agility_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    action_ids = Column(ARRAY(Integer), default=[])
    role_ids = Column(ARRAY(Integer), default=[])
    user_ids = Column(ARRAY(Integer), default=[])
    org_ids = Column(ARRAY(Integer), default=[])
