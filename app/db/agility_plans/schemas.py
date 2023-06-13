from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any
from app.db.enums import MetricsType


class AgilityPlanBase(BaseModel):
    name: str = None
    description: str = None
    actions: Any = None
    leads: Any = None
    sponsors: Any = None
    coreteams: Any = None
    coaches: Any = None
    roles: Any = None
    users: Any = None
    organizations: Any = None
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


class AgilityPlanCreate(AgilityPlanBase):
    name: str
    actions: List[RelatedItemBase] = None
    leads: List[RelatedItemBase] = None
    sponsors: List[RelatedItemBase] = None
    coreteams: List[RelatedItemBase] = None
    coaches: List[RelatedItemBase] = None
    roles: List[RelatedItemBase] = None
    users: List[RelatedItemBase] = None
    organizations: List[RelatedItemBase] = None
    objectives: List[RelatedItemBase] = None

    class Config:
        orm_mode = True


class AgilityPlanEdit(AgilityPlanBase):
    actions: Any = None
    actions: List[RelatedItemBase] = None
    leads: List[RelatedItemBase] = None
    sponsors: List[RelatedItemBase] = None
    coreteams: List[RelatedItemBase] = None
    coaches: List[RelatedItemBase] = None
    roles: List[RelatedItemBase] = None
    users: List[RelatedItemBase] = None
    organizations: List[RelatedItemBase] = None
    objectives: List[RelatedItemBase] = None

    class Config:
        orm_mode = True


class AgilityPlanOut(AgilityPlanBase):
    id: int
    actions: List[RelatedItemBase] = None
    leads: List[RelatedItemBase] = None
    sponsors: List[RelatedItemBase] = None
    coreteams: List[RelatedItemBase] = None
    coaches: List[RelatedItemBase] = None
    roles: List[RelatedItemBase] = None
    users: List[RelatedItemBase] = None
    organizations: List[RelatedItemBase] = None
    objectives: List[RelatedItemBase] = None

    class Config:
        orm_mode = True


class AgilityPlanListOut(AgilityPlanBase):
    id: int
    actions: List[RelatedItemBase] = None
    leads: List[RelatedItemBase] = None
    sponsors: List[RelatedItemBase] = None
    coreteams: List[RelatedItemBase] = None
    coaches: List[RelatedItemBase] = None
    roles: List[RelatedItemBase] = None
    users: List[RelatedItemBase] = None
    organizations: List[RelatedItemBase] = None
    objectives: List[RelatedItemBase] = None

    class Config:
        orm_mode = True
