from sqlalchemy import Column, Integer, Date, String, Boolean

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Table, ForeignKey, Numeric
from app.db.actions.models import Action
from app.db.objectives.models import Objective
from app.db.users.models import User
from app.db.roles.models import Role


class AgilityPlanRelation(Base):
    __tablename__ = "agility_plan_relations"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agility_plan_id = Column(Integer, ForeignKey("agility_plans.id"))
    related_id = Column(Integer)
    relation_type = Column(String)


class AgilityPlanActionRelation(Base):
    __tablename__ = "agility_plan_action_relationship"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agility_plan_id = Column(Integer, ForeignKey("agility_plans.id"))
    action_id = Column(Integer)
    start_time = Column(Date)
    end_time = Column(Date)
    dependency = Column(Integer)


class AgilityPlan(Base):
    __tablename__ = "agility_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)

    actions = relationship(
        "Action",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == Action.id)",
        secondary="agility_plan_relations",
    )
    objectives = relationship(
        "Objective",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == Objective.id)",
        secondary="agility_plan_relations",
    )
    leads = relationship(
        "User",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == User.id)",
        secondary="agility_plan_relations",
    )
    sponsors = relationship(
        "User",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == User.id)",
        secondary="agility_plan_relations",
    )
    coreteams = relationship(
        "User",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == User.id)",
        secondary="agility_plan_relations",
    )
    coaches = relationship(
        "User",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == User.id)",
        secondary="agility_plan_relations",
    )
    users = relationship(
        "User",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == User.id)",
        secondary="agility_plan_relations",
    )
    roles = relationship(
        "Role",
        primaryjoin="and_(AgilityPlanRelation.agility_plan_id == AgilityPlan.id)",
        secondaryjoin="and_(AgilityPlanRelation.related_id == Role.id)",
        secondary="agility_plan_relations",
    )

    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_active = Column(Boolean)
