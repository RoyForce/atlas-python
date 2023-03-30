from app.db.application_types.schemas import ApplicationTypeOut
from pydantic import BaseModel
from datetime import datetime


class ApplicationUrlBase(BaseModel):
    name: str = None
    description: str = None
    url: str = None
    application_type_id: int = None


class ApplicationUrlEdit(ApplicationUrlBase):
    class Config:
        orm_mode = True


class ApplicationUrlOut(ApplicationUrlBase):
    id: int
    application_type: ApplicationTypeOut = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
