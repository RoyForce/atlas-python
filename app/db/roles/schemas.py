from typing import Any, List, Optional
from pydantic import BaseModel
from datetime import datetime


class RoleBase(BaseModel):
    name: str = None
    description: str = None
    job_ids: Optional[List[int]] = []
    playbook_ids: Optional[List[int]] = []
    use_case_ids: Optional[List[int]] = []
    created_at: datetime = None
    updated_at: datetime = None
    source_id: int = None
    source_update_at: datetime = None
    created_by: int = None
    updated_by: int = None
    is_deleted: bool = None


class RoleCreate(RoleBase):
    name: str
    description: str = None

    class Config:
        orm_mode = True


class RoleEdit(RoleBase):
    class Config:
        orm_mode = True


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
