from pydantic import BaseModel
import typing as t
from datetime import datetime


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None
    role_id: int = None
    is_designer: bool = False
    source: str = None
    source_app: str = None
    source_id: int = None
    source_update_at: datetime = None
    cost_center_id: int = None
    is_deleted: bool = None
    created_by: int = None
    updated_by: int = None


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
