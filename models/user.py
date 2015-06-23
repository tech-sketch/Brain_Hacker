import bcrypt
from sqlalchemy import Column, Integer, String, Binary
from sqlalchemy.orm import relationship
from models.base_model import DjangoLikeModelMixin, Base
from models.relations import association_table
from models.group import Group


class User(Base, DjangoLikeModelMixin):
    name = Column(String)
    email = Column(String)
    hashed_password = Column(Binary)
    groups = relationship("Group", secondary=association_table, backref='users')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())

    def json(self):
        return {'name': self.name, 'email': self.email, 'id': self.id}

    def matches_password(self, password):
        return bcrypt.hashpw(password=password.encode('utf-8'), salt=self.hashed_password) == self.hashed_password

    def belongs_to_group(self, group_id):
        for group in self.groups:
            if group_id == group.id:
                return True
        return False


if __name__ == '__main__':
    import sqlalchemy
    from settings import url
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    import bcrypt
    user = User(name="name", email="neko", password="neko")
    session.add(user)
    session.commit()