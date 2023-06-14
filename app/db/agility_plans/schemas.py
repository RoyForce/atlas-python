from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any
from app.db.enums import MetricsType
from app.db.actions.schemas import ActionBase
from app.db.objectives.schemas import ObjectiveBase
from app.db.users.schemas import UserBase
from app.db.roles.schemas import RoleBase


class AgilityPlanBase(BaseModel):
    name: str = None
    description: str = None
    actions: Any = None
    objectives: Any = None

    created_at: datetime = None
    updated_at: datetime = None
    created_by: int = None
    updated_by: int = None


class RelatedItemBase(BaseModel):
    id: int = None
    item_title: str = None
    item_id: int = None
    item_order: int = None
    item_metrics_type: str = None
    item_start_value: int = None
    item_target_value: int = None
    item_action_type: str = None

    class Config:
        orm_mode = True


class Action(BaseModel):
    id: int = None
    title: str = None


class AgilityPlanCreate(AgilityPlanBase):
    name: str = None
    description: str = None
    actions: List[ActionBase] = None
    leads: List[RelatedItemBase]
    sponsors: List[RelatedItemBase]
    coreteams: List[RelatedItemBase]
    coaches: List[RelatedItemBase]
    roles: List[RelatedItemBase]
    users: List[RelatedItemBase]
    organizations: List[RelatedItemBase]
    objectives: List[ObjectiveBase] = None

    class Config:
        orm_mode = True


class AgilityPlanEdit(AgilityPlanBase):
    actions: Any = None
    actions: List[ActionBase]
    leads: List[RelatedItemBase]
    sponsors: List[RelatedItemBase]
    coreteams: List[RelatedItemBase]
    coaches: List[RelatedItemBase]
    roles: List[RelatedItemBase]
    users: List[RelatedItemBase]
    organizations: List[RelatedItemBase]
    objectives: List[ObjectiveBase]

    class Config:
        orm_mode = True


class AgilityPlanOut(AgilityPlanBase):
    id: int
    leads: List[RelatedItemBase]
    sponsors: List[RelatedItemBase]
    coreteams: List[RelatedItemBase]
    coaches: List[RelatedItemBase]
    roles: List[RelatedItemBase]
    users: List[RelatedItemBase]
    organizations: List[RelatedItemBase]

    class Config:
        orm_mode = True


class AgilityPlanListOut(AgilityPlanBase):
    id: int
    leads: List[RelatedItemBase]
    sponsors: List[RelatedItemBase]
    coreteams: List[RelatedItemBase]
    coaches: List[RelatedItemBase]
    roles: List[RelatedItemBase]
    users: List[RelatedItemBase]
    organizations: List[RelatedItemBase]

    class Config:
        orm_mode = True


class AgilityPlan(AgilityPlanBase):
    id: int
    name: str = None
    description: str = None
    actions: List[ActionBase] = None
    objectives: List[ObjectiveBase] = None

    class Config:
        orm_mode = True

    leads: List[RelatedItemBase]
    sponsors: List[RelatedItemBase]
    coreteams: List[RelatedItemBase]
    coaches: List[RelatedItemBase]
    roles: List[RelatedItemBase]
    users: List[RelatedItemBase]
    organizations: List[RelatedItemBase]
