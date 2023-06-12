from app.db.application_types.schemas import ApplicationTypeOut
from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class ApplicationUrlBase(BaseModel):
    name: str = None
    description: str = None
    url: str = None
    application_type_id: int = None
    created_by: int = None
    updated_by: int = None


class ApplicationUrlEdit(ApplicationUrlBase):
    class Config:
        orm_mode = True


class ApplicationUrlOut(ApplicationUrlBase):
    id: int
    application_type: ApplicationTypeOut = None
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True
