from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import DjangoLikeModelMixin, Base
#from group import Group


class Room(Base, DjangoLikeModelMixin):
    name = Column(String)
    group_id = Column(Integer, ForeignKey('group.id'))

if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    room = Room(name="name")
    session.add(room)
    session.commit()