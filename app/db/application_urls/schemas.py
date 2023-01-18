from pydantic import BaseModel
import typing as t


class ApplicationUrlBase(BaseModel):
    name: str
    description: str = None
    url: str = None


class ApplicationUrlCreate(ApplicationUrlBase):
    name: str
    description: str = None

    class Config:
        orm_mode = True


class ApplicationUrlEdit(ApplicationUrlBase):
    class Config:
        orm_mode = True


class ApplicationUrl(ApplicationUrlBase):
    id: int

    class Config:
        orm_mode = True
