from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base
Base = declarative_base()


class DjangoLikeModelMixin(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()