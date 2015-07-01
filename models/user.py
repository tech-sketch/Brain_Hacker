import bcrypt
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, PasswordType
from models.base_model import DjangoLikeModelMixin, Base
from models.relations import association_table
from models.group import Group


class User(Base, DjangoLikeModelMixin):
    name = Column(String(30), nullable=False)
    email = Column(EmailType, nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    groups = relationship("Group", secondary=association_table, backref='users')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {'name': self.name, 'email': self.email, 'id': self.id}

    def verify_password(self, password):
        return self.password == password

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
    user = User(name="admin", email="admin@tis.co.jp", password="admin")
    session.add(user)
    session.commit()