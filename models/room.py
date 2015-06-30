from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import DjangoLikeModelMixin, Base
#from group import Group


class Room(Base, DjangoLikeModelMixin):
    name = Column(String(30))
    theme = Column(String(100))
    group_id = Column(Integer, ForeignKey('group.id'))

    def __init__(self, name, theme):
        self.name = name
        self.theme = theme

if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    room = Room(name="Test Room", theme="brainstorming")
    session.add(room)
    session.commit()