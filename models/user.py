from sqlalchemy import Column, Integer, String, Binary
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.base_model import DjangoLikeModelMixin, Base
from models.relations import association_table
from models.group import Group
#Base = declarative_base()


class User(Base, DjangoLikeModelMixin):
    name = Column(String)
    email = Column(String)
    hashed_password = Column(Binary)
    groups = relationship("Group", secondary=association_table, backref='users')


if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    import bcrypt
    user = User(name="name", email="neko", hashed_password=bcrypt.hashpw("neko".encode("utf-8"), bcrypt.gensalt()))
    session.add(user)
    session.commit()