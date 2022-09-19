# from sqlalchemy.ext.declarative import declared_attr


class CoreBase(object):
    def as_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
