from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import DjangoLikeModelMixin, Base


class Group(Base, DjangoLikeModelMixin):
    from .room import Room
    name = Column(String(30), nullable=False, info={'label': 'グループ名'})
    description = Column(String(100), nullable=False, info={'label': '一言説明'})
    rooms = relationship("Room", backref='groups', cascade='all, delete-orphan',)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def update(self, *args, **kwargs):
        self.name = kwargs.get('name', self.name)
        self.description = kwargs.get('description', self.description)


if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    group = Group(name="STC", description="STC Test")
    session.add(group)
    session.commit()