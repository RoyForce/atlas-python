from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Table, ForeignKey, Numeric
from typing import List, Optional, Any


agility_plan_objective_table = Table(
    "re_agility_plan_objective",
    Base.metadata,
    Column("agility_plan_id", ForeignKey("agility_plans.id")),
    Column("objective_id", ForeignKey("objectives.id")),
)


agility_plan_role_table = Table(
    "re_agility_plan_role",
    Base.metadata,
    Column("agility_plan_id", ForeignKey("agility_plans.id")),
    Column("role_id", ForeignKey("roles.id")),
)


agility_plan_user_table = Table(
    "re_agility_plan_user",
    Base.metadata,
    Column("agility_plan_id", ForeignKey("agility_plans.id")),
    Column("user_id", ForeignKey("user.id")),
)


class AgilityPlan(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "agility_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)

    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_active = Column(Boolean)
