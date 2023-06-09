from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class AgilityPlanBase(BaseModel):
    name: str = None
    description: str = None
    
    created_at: datetime = None
    updated_at: datetime = None


class AgilityPlanCreate(AgilityPlanBase):
    name: str
    action_ids: Optional[List[int]] = []
    role_ids: Optional[List[int]] = []
    user_ids: Optional[List[int]] = []
    org_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class AgilityPlanEdit(AgilityPlanBase):
    action_ids: Optional[List[int]] = []
    role_ids: Optional[List[int]] = []
    user_ids: Optional[List[int]] = []
    org_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class AgilityPlanOut(AgilityPlanBase):
    id: int
    action_ids: Optional[List[int]] = []
    role_ids: Optional[List[int]] = []
    user_ids: Optional[List[int]] = []
    org_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class AgilityPlanListOut(AgilityPlanBase):
    id: int

    class Config:
        orm_mode = True
