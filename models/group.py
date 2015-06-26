from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import DjangoLikeModelMixin, Base



class Group(Base, DjangoLikeModelMixin):
    from .room import Room
    name = Column(String)
    rooms = relationship("Room", backref='groups', cascade='all, delete-orphan',)

if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    group = Group(name="name")
    session.add(group)
    session.commit()