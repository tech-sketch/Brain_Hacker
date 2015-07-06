from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from backend import Backend

Base = declarative_base()


class DjangoLikeModelMixin(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def get(cls, id):
        return cls.session().query(cls).get(id)

    @classmethod
    def search_name(cls, name):
        return cls.session().query(cls).filter(cls.name.ilike('%{0}%'.format(name))).order_by(cls.name).all()

    def save(self):
        self.session().add(self)
        self.session().commit()

    def delete(self):
        self.session().delete(self)
        self.session().commit()

    @staticmethod
    def session():
        return Backend.instance().get_session()