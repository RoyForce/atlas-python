from app.db.application_types.schemas import ApplicationTypeOut
from pydantic import BaseModel
from app.db.roles.schemas import Role
from app.db.application_urls.schemas import ApplicationUrlOut
from typing import List, Any, Dict, AnyStr, Optional
from enum import Enum
from datetime import datetime
from app.db.users.schemas import UserName


class JobSnippetBase(BaseModel):
    name: str = None
    description: str = None
    steps: Dict[AnyStr, Any] = None
    created_by: int = None
    updated_by: int = None


class JobSnippetEdit(JobSnippetBase):
    class Config:
        orm_mode = True


class JobSnippetOut(JobSnippetBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
