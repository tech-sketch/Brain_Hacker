import sqlalchemy
import sqlalchemy.orm
from settings import url
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Backend(object):

    def __init__(self):
        engine = sqlalchemy.create_engine(url, echo=False)
        self._session = sqlalchemy.orm.sessionmaker(bind=engine)()

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    def get_session(self):
        return self._session