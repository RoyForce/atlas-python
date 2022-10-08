# from sqlalchemy.ext.declarative import declared_attr


from typing import List, Union


class CoreBase(object):
    def dict(self, exclude: Union[List[str], None] = []):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }
