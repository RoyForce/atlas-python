from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class ApplicationTypeBase(BaseModel):
    name: str
    description: str = None
    url: str = None
    created_by: int = None
    updated_by: int = None


class ApplicationTypeOut(ApplicationTypeBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
