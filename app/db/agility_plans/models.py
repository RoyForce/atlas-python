from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Table, ForeignKey, Numeric


class AgilityPlanRelation(Base):
    __tablename__ = "agility_plan_relations"
    agility_plan_id = Column(
        Integer, ForeignKey("agility_plans.id"), primary_key=True
    )
    related_id = (Column(Integer),)
    relation_type = (Column(String),)


class Action(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    action_type = Column(String, nullable=False)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_active = Column(Boolean)
    action_type = Column(String)
    extend_existing = True


class Objective(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "objectives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    metrics_type = Column(String, nullable=False)
    start_value = Column(Numeric)
    target_value = Column(Numeric)
    extend_existing = True


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
    extend_existing = True


class Role(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    source_id = Column(Integer, nullable=True)
    extend_existing = True


class AgilityPlan(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "agility_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    actions = relationship(
        "Action",
        secondary="agility_plan_relations",
    )
    objectives = relationship(
        "Objective",
        secondary="agility_plan_relations",
    )
    leads = relationship(
        "User",
        secondary="agility_plan_relations",
    )
    sponsors = relationship(
        "User",
        secondary="agility_plan_relations",
    )
    coreteams = relationship(
        "User",
        secondary="agility_plan_relations",
    )
    coaches = relationship(
        "User",
        secondary="agility_plan_relations",
    )
    roles = relationship(
        "Role",
        secondary="agility_plan_relations",
    )
    users = relationship(
        "User",
        secondary="agility_plan_relations",
    )
    organizations = relationship(
        "User",
        secondary="agility_plan_relations",
    )
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_active = Column(Boolean)
