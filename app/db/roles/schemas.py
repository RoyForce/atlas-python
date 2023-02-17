from pydantic import BaseModel
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str = None
    created_at: datetime = None
    updated_at: datetime = None


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
