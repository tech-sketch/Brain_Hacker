from sqlalchemy import Column, String
#from sqlalchemy.ext.declarative import declarative_base
from models.base_model import DjangoLikeModelMixin, Base
#Base = declarative_base()


class Group(Base, DjangoLikeModelMixin):
    name = Column(String)


if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    group = Group(name="name")
    session.add(group)
    session.commit()