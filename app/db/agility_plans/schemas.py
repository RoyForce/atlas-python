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
    created_by: int = None
    updated_by: int = None


class RelatedItemBase(BaseModel):
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
    title: str = None


class AgilityPlanCreate(AgilityPlanBase):
    name: str = None
    description: str = None
    actions: List[int] = None
    lead_ids: List[int] = None
    sponsor_ids: List[int] = None
    coreteam_ids: List[int] = None
    coach_ids: List[int] = None
    role_ids: List[int] = None
    user_ids: List[int] = None
    objectives: List[int] = None

    class Config:
        orm_mode = True


class AgilityPlanEdit(AgilityPlanBase):
    actions: Any = None
    objectives: List[int]
    lead_ids: List[int]
    sponsor_ids: List[int]
    coreteam_ids: List[int]
    coach_ids: List[int]
    role_ids: List[int]
    user_ids: List[int]

    class Config:
        orm_mode = True


class AgilityPlanActionCreate(BaseModel):
    agility_plan_id: int
    name: Any
    type: str
    start_date: str
    end_date: str
    dependency: int

    class Config:
        orm_mode = True


class AgilityPlanOut(AgilityPlanBase):
    id: int
    lead_ids: List[RelatedItemBase]
    sponsor_ids: List[RelatedItemBase]
    coreteam_ids: List[RelatedItemBase]
    coach_ids: List[RelatedItemBase]
    role_ids: List[RelatedItemBase]
    user_ids: List[RelatedItemBase]

    class Config:
        orm_mode = True


class AgilityPlanListOut(AgilityPlanBase):
    id: int
    lead_ids: List[RelatedItemBase]
    sponsor_ids: List[RelatedItemBase]
    coreteam_ids: List[RelatedItemBase]
    coach_ids: List[RelatedItemBase]
    role_ids: List[RelatedItemBase]
    user_ids: List[RelatedItemBase]

    class Config:
        orm_mode = True


class AgilityPlan(AgilityPlanBase):
    name: str = None
    description: str = None
    actions: List[ActionBase] = None
    objectives: List[ObjectiveBase] = None
    lead_ids: List[RelatedItemBase]
    sponsor_ids: List[RelatedItemBase]
    coreteam_ids: List[RelatedItemBase]
    coach_ids: List[RelatedItemBase]
    role_ids: List[RelatedItemBase]
    user_ids: List[RelatedItemBase]

    class Config:
        orm_mode = True
