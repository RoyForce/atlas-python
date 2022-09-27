from pydantic import BaseModel
import typing as t


class ApplicationUrlBase(BaseModel):
    name: str
    url: str = None


class ApplicationUrlOut(ApplicationUrlBase):
    pass


class ApplicationUrlCreate(ApplicationUrlBase):
    name: str

    class Config:
        orm_mode = True


class ApplicationUrlEdit(ApplicationUrlBase):
    class Config:
        orm_mode = True


class ApplicationUrl(ApplicationUrlBase):
    id: int

    class Config:
        orm_mode = True
